#!/usr/bin/python

import os
import sys

sys.path.append('/home/coursework/Assignments/Program1')
import ShopBuilder

print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Shopper Login Screen</title>"
print "</head>"

print "<body>"
print "<h1>Please log in</h1>"
print "<form>"
print "User ID:<input type='text' id='userid'><br>"
print "Password:<input type='password' id='passwd'><br>"
print "<input type='submit' value='Login'><br>"
print "<p><a href="">Register as a new user</a></p>"
print "</form>"
print "</body>"
print "</html>"
