#!/usr/bin/python

'''
The purpose of this script is to allow the user to login to the system.
Both username and password are required to go anywhere.
If the user attempts to login, the script proceeds to the login_verification script.
The user can also click the register a new user hyperlink. Which, will send them
to the registration page.
'''

import os
import sys
import cgi

sys.path.append('/home/coursework/public_html/Builder/')
import ShopBuilder

print """Content-type:text/html\r\n\r\n
<html>
<head>
<title>Shopper Login Screen</title>
</head>

<body>
<h1>Please log in</h1><br>
<form name='login' action='http://localhost/~coursework/cgi-bin/login_verification.cgi' method='POST'>
User ID:<input type='text' name='userident' value="" style="margin-left:50px;" required><br>
Password:<input type='password' name='user_passwd' value=""style="margin-left:32px;" required><br>
<input type='submit' value='Login'><br><br>
<p><a href='http://localhost/~coursework/cgi-bin/registration.cgi'>Register as a new user</a></p>
</form>
</body>
</html>"""


