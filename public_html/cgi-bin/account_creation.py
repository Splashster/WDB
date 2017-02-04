#!/usr/bin/python

import cgi
import user_verification

form_items = cgi.FieldStorage()
userid = form_items.getvalue('user_id')
f_name = form_items.getvalue('first_name')
l_name = form_items.getvalue('last_name')
email_add = form_items.getvalue('email')
user_pass = form_items.getvalue('passwd')

if userid is None:
	userid = ""
if f_name is None:
	f_name = ""
if l_name is None:
	l_name = ""
if email_add is None:
	email_add = ""
if user_pass is not None:
	print """Content-type:text/html\r\n\r\n
	  	<html>
		<body>"""
	try:	
		user_verification.validate(userid, f_name, l_name, user_pass, email_add )
		print """<script type='text/javascript'>
		alert('Account Succesfully Created!')
		window.location.href='http://localhost/~coursework/cgi-bin/userlogin.cgi'
		</script>"""
	except:
		print """
		<script type='text/javascript'>
		alert('User ID already exists')
		window.location.href='http://localhost/~coursework/cgi-bin/registration.cgi?first_name=%s&last_name=%s&user_id=%s&email=%s'
		</script>
		"""%(f_name,l_name,userid,email_add)
	print """
		</body>
		</html>"""

