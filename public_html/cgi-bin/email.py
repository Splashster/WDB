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
useriden = form_items.getvalue('userid')
items = form_items.getvalue('items')

#useriden = '123'
#items = {"CH1203":1}

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
	quantity.append(items[k])
	item_result = cursor.fetchall()
	item = (item_result + quantity)
	purchased_item.append(item)
	purchased_items.append(purchased_item)
	
print purchased_items


print """Content-type:text/html\r\n\r\n
<html>
<body>
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

for(i in %s){
console.log(i)
}"""%(purchased_items)
print """
removeCookies();

</script>
</body>
</html>"""
