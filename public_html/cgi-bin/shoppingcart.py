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
index = 0
rowcount = 0
quantity = 0

print """Content-type:text/html\r\n\r\n
<html>
<head>
<h1 align="center">Catalog<h1>
<style>
table, th, td{
	border: 1px solid black;
}
</style>
<script type="text/javascript">
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

function checkCookie() {
var user=getCookie("username")
var quantities = JSON.parse( getCookie("cart_items"))
console.log(quantities);
if(user != " "){
	alert('Welcome ' + quantities["C12345R"] + '!');
}else{
	alert('Dont know who you are!');
}}
function addItems(){
var purchases = []
var items = {}"""
for r in results:
	print """
	items["%s"]=document.getElementById("quantity"+"%s").value;
	"""%(r[0],rowcount)
	rowcount+=1
print """
purchases.push(JSON.stringify(items));
console.log(purchases)
createCookie("cart_items",purchases,30);
checkCookie();	
}
</script>
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
		var row = table.insertRow(-1);
		var cell1 = row.insertCell(0);
		var cell2 = row.insertCell(1);
		var cell3 = row.insertCell(2);
		var cell4 = row.insertCell(3);
		var cell5 = row.insertCell(4);
		var cell6 = row.insertCell(5);
		cell1.innerHTML = '%s';
		cell2.innerHTML = '%s';
		cell3.innerHTML = '%s';
		cell4.innerHTML = '%s';
		cell5.innerHTML = '0';
		quant=document.createElement("input");
		quant.id="quantity"+'%s';
		cell6.appendChild(quant);
		document.getElementById(quant.id).defaultValue=0;
		document.getElementById(quant.id).type="number";
		document.getElementById(quant.id).required=true;
		document.getElementById(quant.id).style.width = "100%%";
		document.getElementById(quant.id).style.textAlign = "center";
		</script>
		"""%(res_row[0], res_row[1], res_row[2], res_row[3], index)
	index+=1
print """
	</table>
	<button type="button">Checkout</button>
	<button type="button" onclick=addItems()>Add Item</button>
	
	</body>
	</html>"""
