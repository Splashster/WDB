#!/usr/bin/python

from json import dumps

import sys
import os
import cgi

sys.path.append('/home/coursework/Assignments/Program1')

import mysql.connector
from Database import *


con = mysql.connector.connect(user=user, password=passwd, host=host, database=db)
cursor = con.cursor(buffered=True)

'''
Validate that the User's ID has not already been taken
'''
def validateUserID(userid):
	cursor.execute(("select * from UserAccounts where `id` = %s"), (userid,))
	print cursor.rowcount
	count = cursor.rowcount
	if count >= 1:
		return False;
	else:
		return True;

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Shopper Registration Screen</title>"
print "</head>"

print "<body>"
print "<h1>Registration</h1><br>"
#print "<form action='http://localhost/~coursework/cgi-bin/pass_verification.py' method='post'>"
print "<form name='reg'>"
print "First Name: <input type='text' name='first_name' required><br>"
print "Last Name: <input type='text' name='last_name' required><br>"  
print "User ID: <input type='text' name='user_id' required><br>"
print "Password: <input type='password' name='passwd' required><br>"
print "Confirm Password: <input type='password' name=conf_passwd required><br>"
print "Email: <input type='text' name='email' required><br>"
print "<input type = 'submit' onclick='return validateInformation();' value='Register'/>"
print "<script type='text/javascript'>"
print "function validateInformation(){"
form_items = cgi.FieldStorage()
userid = form_items.getvalue('user_id')
valid_user = validateUserID(userid)
#print userid, valid_user
print "if('''+valid_user+'''  == false){ reg.user_id.setCustomValidity('User ID already taken')}"  
print "else if(reg.passwd.value != reg.conf_passwd.value){"
print "reg.conf_passwd.setCustomValidity('Passwords Do not Match!');} else {"
print "reg.conf_passwd.setCustomValidity(''); return true;}}"
print "</script>"
print "</form>"
print "</body>"
print "</html>"

cursor.close()
con.close()
