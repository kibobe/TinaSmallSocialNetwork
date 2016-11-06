#!/usr/bin/python

import MySQLdb
import json


db1 = MySQLdb.connect(host="localhost",user="root",passwd="pucam500")
cursor = db1.cursor()

try:
    sql = 'CREATE DATABASE IF NOT EXISTS socialNetwork'
    cursor.execute(sql)
except:
    print "Can not create database"
    exit()
  
try:
    db1 = MySQLdb.connect("localhost","root","pucam500","socialNetwork" )
    cursor = db1.cursor()
except:
    print "Bad connection"
    exit()
  

#create two tables, people and friends  
try:  
    sql = ('CREATE TABLE IF NOT EXISTS people('
	  ' id INT NOT NULL,'
	  ' firstName VARCHAR(10),'
	  ' surname VARCHAR(20),'
	  ' age INT,'
	  ' gender VARCHAR(10),'
	  ' PRIMARY KEY(id))')
    cursor.execute(sql)
except:
    print "Can not create table people"
    exit()

try:    
    sql = ('CREATE TABLE IF NOT EXISTS friends('
	  ' id INT NOT NULL,'
	  ' friend_id INT NOT NULL, '
	  ' CONSTRAINT pk_id PRIMARY KEY (id,friend_id))')
    cursor.execute(sql)
except:
    print "Can not create table friends"

with open('data.json') as data_file:    
      data = json.load(data_file)

#insert into table people
for row in data:
      sql = ('INSERT INTO people(id, firstName, surname, age, gender)'
	    ' VALUES(%s, %s, %s, %s, %s)')
      args = (row['id'], row['firstName'], row['surname'], row['age'], row['gender'])
      try:
	cursor.execute(sql,args)
	db1.commit()
      except:
	db1.rollback()
	
      #insert into table friends	
      friends = row['friends']
      for friend_id in friends:
	  sql = ('INSERT INTO friends(id, friend_id)'
		' VALUES(%s, %s)')
	  args = (row['id'], friend_id)
	  try:
	      cursor.execute(sql,args)
	      db1.commit()
	  except:
	      db1.rollback()

db1.close()