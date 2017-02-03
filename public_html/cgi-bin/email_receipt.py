#!/usr/bin/python

import cgi
import os
import sys
import mysql.connector
import json
import smtplib


def sendEmail(purchased_items,total,first_name,last_name):
	sender = 'coursework@coursework.csc.tntech.edu'
	receiver = 'coursework@coursework.csc.tntech.edu'
	
	index = 0
	purchased_items = purchased_items.split(",")
	purchased_item = []
	total_item = []
	for i in purchased_items:
		purchased_item.append(i)
		if(index == 3):
			total_item.append(purchased_item)
			purchased_item = []
			index = 0
		else:
			index+=1
	
	msg = """From: Awesome Sales<coursework@coursework>
	To: To %s %s  <coursework@coursework>
	Subject: Receipt of Purchase

Hello %s %s,

Thank you for shoping at Awesome Sales!
We value your time and hope you found everything you were looking for!
Below is the total amount you have been charged. For a more detailed receipt,
please refer back to the checkout page. If you are unable to get this information, just call us.

	Purchased Items
"""%(first_name, last_name, first_name, last_name)
	row_headers = ["Product ID", "Product Name", "Price Each", "Quantity Purchased"];
	for row in row_headers:
		msg+= """\t%s"""%("{:<18}".format(row))
	msg+="\n"	
	for s in total_item:
		for x in s:
			msg+= """\t%s"""%("{:<20}".format(x))
		msg+="\n"
	msg+="""

	Total: %s

Please come back and see us!

Sincerely,
	

Awesome Sales Team
"""%(total)

	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender,receiver, msg)
		
	except smtplib.SMTPException:
		pass

if __name__ == '__main__':
	sendEmail()


