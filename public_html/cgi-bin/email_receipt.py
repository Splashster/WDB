#!/usr/bin/python

import cgi
import os
import sys
import mysql.connector
import json
import smtplib


def sendEmail():
	sender = 'coursework@coursework.csc.tntech.edu'
	receiver = 'coursework@coursework.csc.tntech.edu'

	msg = """From: Awesome Sales<coursework@coursework>
	To: To Person <coursework@coursework>
	Subject: Purchase Receipt


	Thank you for shoping at Awesome Sales!
	We value you time and hope you found everything you were looking for!
	Below is a copy of your receipt
	Please come back and see us!

	Sincerely,


	Awesome Sales Team
	"""
	try:
		smtpObj = smtplib.SMTP('localhost')
		smtpObj.sendmail(sender,receiver, msg)
		
	except smtplib.SMTPException:
		pass

if __name__ == '__main__':
	sendEmail()


