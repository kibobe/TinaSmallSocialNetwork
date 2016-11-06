#!/usr/bin/python
import MySQLdb
import string
import re,sys

class Network():
    
    def __init__(self):
	self.db = None
	try:
	    self.db = MySQLdb.connect("localhost","root","pucam500","socialNetwork")
	    self.cursor = self.db.cursor()
	except:
	    print "Bad connection \n Something is wrong"
	    exit()
	    
	
    def getAllUsers(self):
	 
	listUsers = []
	self.cursor = self.db.cursor()
	sql= ('SELECT CONCAT(firstName, \' \', surname) FROM people')
	
	try:
	    self.cursor.execute(sql)
	    resultNameOfPeople = self.cursor.fetchall()
	    for oneUser in resultNameOfPeople:
		listUsers.append(str(oneUser[0]))
	    
	    return listUsers
	except:
	    print "Error: unable to fecth data"
	    
    	      
    def getIdFromName(self, myName):
       
	nameAndSurname=re.split(" ", str(myName))
	self.cursor = self.db.cursor()
       
	sql = ("SELECT id FROM people"
	     " WHERE firstName like %s and surname like %s")
	args = (nameAndSurname[0], nameAndSurname[1])

	try:
	    self.cursor.execute(sql,args)
	    resultId = self.cursor.fetchall()
	except:
	    print "Error: unable to fecth data"
       
	return resultId[0][0]
       
    
    def getListResultPeople(self, sql, args):
	
	listOfPeople=[]
	self.cursor = self.db.cursor()

	try:
	    numberFriend = self.cursor.execute(sql,args)
	    resultPeoplesId = self.cursor.fetchall()
	    if numberFriend == 0:
		listOfPeople.append("No results")
		    
	    for oneUserId in resultPeoplesId:
		sql = ('SELECT firstName, surname, age, gender from people'
			' WHERE id = %s')
		args = (str(oneUserId[0]))
		try:
		    self.cursor.execute(sql,args)
		    resultsNames = self.cursor.fetchall()
			
		    for oneUser in resultsNames:
			fullName = str(" ")
			for partName in oneUser: 
			    if partName is not None:
				fullName += str(partName)
				fullName += str(" ")
			listOfPeople.append(fullName)
		except:
		    print "Error: unable to fecth data"
            return listOfPeople
	except:
	    print "Error: unable to fecth data"
       

    def getFriends(self, myName):
	
	myId = self.getIdFromName(myName)
	
	sql = ('SELECT id from friends'
	      ' WHERE friend_id = %s')
	args = (str(myId))
	listOfPeople = self.getListResultPeople(sql,args)
	
	return listOfPeople
    
    
    def getFriendOfFriends(self, myName):
	
	myId = self.getIdFromName(myName)
	
	sql = ('SELECT distinct id FROM friends'
		   ' WHERE friend_id in (SELECT id FROM friends '
			    'WHERE friend_id = %s )'
		   ' and id != %s')
	args = (str(myId), str(myId))
	listOfPeople = self.getListResultPeople(sql,args)
	
	return listOfPeople
    
    
    def getSuggestedFriend(self, myName) :
       
	myId = self.getIdFromName(myName)
	
	sql = ('SELECT distinct id, count(friend_id) from friends'
		' where friend_id in (select friend_id from friends' 
				    ' where id=%s )' 
		' and id != %s'
		' and id not in (select friend_id from friends' 
				' where id=%s )'
		' group by id' 
		' having count(friend_id) > 1' )
	args = (str(myId), str(myId), str(myId))
	listOfPeople = self.getListResultPeople(sql,args)
	
	return listOfPeople
      
