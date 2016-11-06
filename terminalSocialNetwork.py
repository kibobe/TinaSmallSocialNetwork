#!/usr/bin/python
import MySQLdb
import string

# print data about people from given query
def printPeopleFromQuery(sql, args):
    try:
	cursor.execute(sql,args)
	results = cursor.fetchall()
	
	for row in results:
	    sql = ('SELECT firstName, surname, age, gender FROM people'
		  ' WHERE id = %s')
	    args = (row[0])
	    try:
		cursor.execute(sql,args)
		results2 = cursor.fetchall()
		
		for row2 in results2:
		    print "name:", row2[0].rjust(10), "\tsurname: ", row2[1].rjust(15), "\tage: ", row2[2], "gender: ", row2[3].rjust(7)
	    except:
		print "Error: unable to fecth data"
	    	  
    except:
	print "Error: unable to fecth data"




# open database connection
db = MySQLdb.connect("localhost","root","pucam500","socialNetwork")

# prepare a cursor object
cursor = db.cursor()

x = raw_input("Enter firstname: ")
y = raw_input("Enter surame: ")

sql = ("SELECT id FROM people"
      " WHERE firstName like %s and surname like %s")
args = (x,y)

# number of people with given name
count = 0
# id of a man with given name
myId = 0

try:
    count = cursor.execute(sql,args)
    results = cursor.fetchall()
    
    for row in results:
	myId = row[0]
except:
    print "Error: unable to fecth data"


if count == 0:
    print x , " ", y, " don't have a social Network "
    exit()    
elif count > 1:
    print "There are more people with name: ", x ,"and surname: ", y
    exit();


print "\n\tFriends:"

sql = ('SELECT id FROM friends'
      ' WHERE friend_id = %s')
args = (myId)
printPeopleFromQuery(sql,args)



print "\n\tFriends of friends:"

sql = ('SELECT distinct id FROM friends'
      ' WHERE friend_id in (SELECT id FROM friends '
			    'WHERE friend_id = %s )'
      ' and id != %s')
args = (myId,myId)
printPeopleFromQuery(sql,args)


print "\n\tSuggested friends:"

sql = ('SELECT distinct id, count(friend_id) from friends'
      ' where friend_id in (select friend_id from friends' 
			  ' where id=%s )' 
      ' and id != %s'
      ' and id not in (select friend_id from friends' 
		     ' where id=%s )'
      ' group by id' 
      ' having count(friend_id) >= 2' )

args = (myId, myId, myId)
printPeopleFromQuery(sql,args)


# disconnect from server
db.close()
