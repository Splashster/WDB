#!/usr/bin/python
import email_receipt

print """Content-type:text/html\r\n\r\n
	<html>
	<body>
	<p> Email Sent</p>
	</body>
	</html>"""

email_receipt.sendEmail()
