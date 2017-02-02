#!/usr/bin/python

import os
import sys
import cgi

sys.path.append('/home/coursework/Assignments/Program1')
import ShopBuilder

print """Content-type:text/html\r\n\r\n
<html>
<head>
<title>Shopper Login Screen</title>
</head>

<body>
<h1>Please log in</h1><br>
<form name='login' action='http://localhost/~coursework/cgi-bin/login_verification.py' method='GET'>
User ID:<input type='text' name='userident' value=""  required><br>
Password:<input type='password' name='user_passwd' value="" required><br>
<input type='submit' value='Login'><br><br>
<p><a href='http://localhost/~coursework/cgi-bin/registration.py'>Register as a new user</a></p>
</form>
</body>
</html>"""


