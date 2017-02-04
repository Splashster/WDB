#!/usr/bin/python

import sys
import os
import mysql.connector

sys.path.append('/home/coursework/public_html/Builder/')

from Database import *

def validate(userid, f_name, l_name, userpass, email_add):
	'''
	Validate that the User's ID has not already been taken
	'''

	con = mysql.connector.connect(user=user, password=passwd, host=host,
	 database=db)
	cursor = con.cursor()
	command = "INSERT INTO `UserAccounts` (id, first_name, last_name, password, email) VALUES (%s,%s,%s,%s,%s)"
	cursor.execute(command, (userid,f_name,l_name,userpass,email_add))
	con.commit()
	cursor.close()
	con.close()

if __name__ == "__main__":
	validate()
