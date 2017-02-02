#!/usr/bin/python

import cgi
from account_creation import *


print"""Content-type:text/html\r\n\r\n
<html>
<head>
<title>Shopper Registration Screen</title>
</head>
<body>
<h1>Registration</h1><br>
<form name='reg' action='http://localhost/~coursework/cgi-bin/account_creation.py' method='get'>
First Name: <input type='text' name='first_name' value="%s" requiredbr>
Last Name: <input type='text' name='last_name' value="%s" required><br>  
User ID: <input type='text' name='user_id' value="%s" required><br>
Password: <input type='password' name='passwd' required><br>
Confirm Password: <input type='password' name=conf_passwd required><br>
Email: <input type='text' name='email' value="%s" required><br>
<input type = 'submit' onclick='return validateInformation();' value='Register'/>
<script type='text/javascript'>
function validateInformation(){
if(reg.passwd.value != reg.conf_passwd.value){
reg.conf_passwd.setCustomValidity('Passwords Do not Match!');} else {
reg.conf_passwd.setCustomValidity(''); return true;}}</script>
</form>
</body>
</html>
"""%(f_name,l_name,userid,email_add)

