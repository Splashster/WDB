#!/usr/bin/python

import cgi
import os
import sys
import mysql.connector

sys.path.append('/home/coursework/Assignments/Program1/')

from Database import *

con = mysql.connector.connect(user=user, password=passwd, host=host, database=db)
cursor = con.cursor(buffered=True)

form_items = cgi.FieldStorage()
useriden = form_items.getvalue('userident')
user_pass = form_items.getvalue('user_passwd')

command = "SELECT * FROM `UserAccounts` where id=%s and password=%s"
cursor.execute(command, (useriden, user_pass))
result = cursor.fetchall()
if cursor.rowcount == 1:
	print """Content-type:text/html\r\n\r\n
	  	<html>
		<body>
		<script type='text/javascript'>
		alert('Login Successful!')
		window.location.href = 'http://localhost/~coursework/cgi-bin/shoppingcart.py'
		</script>
		</body>
		</html>"""
else:
	print """Content-type:text/html\r\n\r\n
		<html>
		<body>
		<script type='text/javascript'>
		alert('Username/Password is Incorrect!')
		</script>
		</body>
		</html>"""

cursor.close()
con.close()
