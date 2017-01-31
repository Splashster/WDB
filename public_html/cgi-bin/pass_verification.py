#!/usr/bin/python

import cgi
import sys
import os

sys.path.append('/home/coursework/Assignments/Program1')

form = cgi.FieldStorage()
passwd = form.getvalue('passwd')
conf_passwd = form.getvalue('conf_passwd')

if passwd == conf_passwd:
	print "Content-type:text/html \r\n\r\n"
	print "<html>"
	print "<head></head>"
	print "<body>"
	print passwd, conf_passwd
	print "</body>"
	print "</html>"
else:
	print "Content-type:text/html \r\n\r\n"
	print "<html>"
	print "<head></head>"
	print "<body>"
	print passwd, conf_passwd
	print "<script type=text/javascript>"
	print "alert('Incorrect Password!')"
	print "</script>"
	print "</body>"
	print "</html>"
