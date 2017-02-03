#!/usr/bin/python

import cgi
import os
import sys
import mysql.connector

sys.path.append('/home/coursework/Assignments/Program1/')

from Database import *


con = mysql.connector.connect(user=user, password=passwd, host=host, database=db)
cursor = con.cursor(buffered=True)


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
function removeCookies(){
	createCookie("username","",-1);
	createCookie("cart_items","",-1);
}
function addItems(){
var purchases = []
var items = {}
var quan"""
for r in results:
	print """
	quan = document.getElementById("quantity"+"%s").value;
	document.getElementById("quantity"+"%s").value = 0;
	in_cart =  document.getElementById("shop_tb").rows[%s].cells[4].innerText;
	total_in_cart = parseInt(in_cart) + parseInt(quan);
	if(total_in_cart < 0){
		total_in_cart = 0;
	}
	document.getElementById("shop_tb").rows[%s].cells[4].innerHTML = total_in_cart;
	items["%s"]=total_in_cart;
	
	"""%(rowcount,rowcount,rowcount+1,rowcount+1,r[0])
	rowcount+=1
print """
purchases.push(JSON.stringify(items));
createCookie("cart_items",purchases,30);
}
function checkOut(){
var useriden = getCookie("username");
try{	
	var final_list = {};
	var cart = JSON.parse(getCookie("cart_items"));
	for(i in cart){
		console.log(cart[i]);
		if(cart[i] > 0){
			final_list[i]=cart[i];
		}
	}
	window.location.href='http://localhost/~coursework/cgi-bin/checkout.py?userid='+useriden+'&items='+JSON.stringify(final_list);
}catch(e){}}
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
		var quan = "";
		try{
			var quantities = JSON.parse( getCookie("cart_items"));
			quan = quantities['%s'];
		}catch(e){}
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
		if(quan == "" || quan === undefined){
			cell5.innerHTML = '0';
		}else{
			cell5.innerHTML = quan;
		}
		quant=document.createElement("input");
		quant.id="quantity"+'%s';
		cell6.appendChild(quant);
		document.getElementById(quant.id).defaultValue=0;
		document.getElementById(quant.id).type="number";
		document.getElementById(quant.id).required=true;
		document.getElementById(quant.id).style.width = "100%%";
		document.getElementById(quant.id).style.textAlign = "center";
		</script>
		"""%(res_row[0],res_row[0], res_row[1], res_row[2], res_row[3], index)
	index+=1
print """
	</table>
	
	<button type="button" onclick=checkOut()>Checkout</button>"""
print"""
	<button type="button" onclick=addItems()>Add Item</button>
	
	</body>
	</html>"""
