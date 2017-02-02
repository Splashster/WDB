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

command = "SELECT * FROM `Inventory`"
cursor.execute(command)
results = cursor.fetchall()

print """Content-type:text/html\r\n\r\n
	<html>
	<head>
	<style>
	table, th, td{
		border: 1px solid black;
	}
	</style>
	</head>
	<body>
	<table id='shop_tb' style="width:100%">
	<tr>
	<th>Product Id</th>
	<th>Product Name</th>
	<th>Description</th>
	<th>Price ea.</th>
	<th>In Cart</th>
	<th>Quan. to Add</th>
	</tr>
	"""
for res_row in results:
	print """
		<script type='text/javascript'>
		var table = document.getElementById('shop_tb');
		var row = table.insertRow(0);
		var cell1 = row.insertCell(0);
		cell1.innerHTML = %s
		</script>
		"""%(res_row[1])
	print """
		</table>
		</body>
		</html>"""
