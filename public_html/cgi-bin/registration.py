#!/usr/bin/python


print "Content-type:text/html\r\n\r\n"
print "<html>"
print "<head>"
print "<title>Shopper Registration Screen</title>"
print "</head>"

print "<body>"
print "<h1>Registration</h1><br>"
print "<form action='http://localhost/~coursework/cgi-bin/pass_verification.py' method='post'>"
print "First Name: <input type='text' name='first_name'><br>"
print "Last Name: <input type='text' name='last_name'><br>"  
print "User ID: <input type='text' name='user_id'><br>"
print "Password: <input type='password' name='passwd'><br>"
print "Confirm Password: <input type='password' name=conf_passwd><br>"
print "Email: <input type='text' name='email'><br>"
print "<input type='submit' value='Register '>"
print "</form>"
print "</body>"
print "</html>"
