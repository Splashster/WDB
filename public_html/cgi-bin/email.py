#!/usr/bin/python

import cgi
import os
import sys
import mysql.connector
import json

sys.path.append('/home/coursework/Assignments/Program1/')

from Database import *


con = mysql.connector.connect(user=user, password=passwd, host=host, database=db)
cursor = con.cursor(buffered=True)

form_items = cgi.FieldStorage()
#useriden = form_items.getvalue('userid')
#items = json.loads(form_items.getvalue('items'))

useriden = '123'
items = {"CH1203":1,"KIJ232103":1}

command = "SELECT * FROM `UserAccounts` where id=%s"
cursor.execute(command, (useriden,))
userinfo = cursor.fetchall()
total_price = 0
purchased_item = []
purchased_items = []
quantity = []
for k in items:
	command = "SELECT id, prod_name,price FROM `Inventory` where id=%s"
	cursor.execute(command,(k,))
	for i in cursor.fetchall():
		if(k == i[0]):
			purchased_item.append(i[0].encode('ascii'))
			purchased_item.append(i[1].encode('ascii'))
			purchased_item.append(i[2].encode('ascii'))
			purchased_item.append(items[k])
			purchased_items.append(purchased_item)
	purchased_item=[]
	


print """Content-type:text/html\r\n\r\n
<html>
<head>
<title>Checkout Screen</title>
</head>
<body>
<h1 align="center">Chcekout</h1>
<p>Thank you for shoping at Awesome Sales!</p>
<p>We value you time and hope you found everything you were looking for!</p>
<p>Below is a copy of your receipt</p>
<p>Please come back and see us!</p>
<script type='text/javascript'>
function createCookie(cname,cvalue,expiretime){
var d = new Date();
d.setTime(d.getTime() + (expiretime*24*60*60*1000));
var expires = "expires=" + d.toGMTString();
document.cookie = cname + "=" + cvalue + ";" + expires + ";path=/";
}
function getCookie(cname) {
var name = cname + "=";
var decodedCookie = decodeURIComponent(document.cookie);
var ca = decodedCookie.split(';');
for(var i = 0; i < ca.length; i++){
var c = ca[i];
while (c.charAt(0) == ' '){
	c = c.substring(1);
}
if(c.indexOf(name) == 0){
	return c.substring(name.length, c.length);
} } return " "; }
function removeCookies(){
	createCookie("username","",-1);
	createCookie("cart_items","",-1);
}

removeCookies();
console.log(%s)"""%(purchased_items)
print """
</script>
<style>
table {
	width:100%;
}
table, th, td {
	border: 1px solid black;
	border-collapse: collapse;
}
th, td {
	padding: 5px;
	text-align:left;
}
tr {
	background-color:#eee;
}
th {
	background-color:black;
	color:white;
}
</style>
<table id='checkout_tb' style="width:100%">
<tr>
<th>Product Id</th>
<th>Product Name</th>
<th>In Cart</th>
<th>Total</th>
</tr>
<script type='text/javascript'>
var item_total = 0;
var item_price = 0;
var sale_total = 0;
"""
for i in purchased_items:
	print """
	var table = document.getElementById('checkout_tb');
	var row = table.insertRow(-1);
	var cell1 = row.insertCell(0);
	var cell2 = row.insertCell(1);
	var cell3 = row.insertCell(2);
	var cell4 = row.insertCell(3);
	cell1.innerHTML = '%s';
	cell2.innerHTML = '%s';
	cell3.innerHTML = '%s';
	item_price = "%s";
	item_total = Number(item_price.replace(/[^0-9\.]+/g,""));
	item_total = parseFloat(item_total) * %s;
	cell4.innerHTML = item_total;
	sale_total= sale_total + item_total;
"""%(i[0],i[1],i[3],i[2], i[3])
print"""

	var table = document.getElementById('checkout_tb');	
	var cell4 = row.insertCell(4);
	cell4.innerHTML = sale_total.toFixed(2);
</script>
</table>
</body>
</html>"""
