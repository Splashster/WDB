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

#useriden = '123'
#user_pass = '123'

command = "SELECT * FROM `UserAccounts` where id=%s and password=%s"
cursor.execute(command, (useriden, user_pass))
result = cursor.fetchall()
if cursor.rowcount == 1:
	print """Content-type:text/html\r\n\r\n
	  	<html>
		<head>
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
		function checkCookie() {
		var user=getCookie("username");
		createCookie("username",user,-1);
		if(user != ""){
			alert('Welcome ' + user + '!');
		}else{
			alert('Dont know who you are!');
		}}
		createCookie("username",'%s',1);
		checkCookie();	
		window.location.href = 'http://localhost/~coursework/cgi-bin/shoppingcart.py'
		</script>
		</head>
		<body>
		</body>
		</html>"""%(useriden)
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
