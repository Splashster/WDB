#!/usr/bin/python

import cgi
import os
import sys
import mysql.connector
import json
import smtplib


def sendEmail(purchased_items,total):
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
	To: To Person <coursework@coursework>
	Subject: Receipt of Purchase


	Thank you for shoping at Awesome Sales!
	We value your time and hope you found everything you were looking for!
	Below is the total amount you have been charged. For a more detailed receipt,
	please refer back to the checkout page. If you are unable to get this information, just call us.

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


