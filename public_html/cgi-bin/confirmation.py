#!/usr/bin/python
import email_receipt
import cgi

form_items = cgi.FieldStorage()
items = form_items.getvalue('purchased_items')
sale_total = form_items.getvalue('total')

	
print """Content-type:text/html\r\n\r\n
	<html>
	<body>
	<p> Email Sent</p>
	%s
	</body>
	</html>"""%(sale_total)

email_receipt.sendEmail()
