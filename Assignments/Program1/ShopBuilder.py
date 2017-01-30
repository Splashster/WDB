import mysql.connector 
from mysql.connector import errorcode
from Database import *

'''
Create shop database if it does not exist
'''
def create_db(cursor):
	try:
		cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db))
	except mysql.connector.Error as err:
		print "Failed creating datbase: {}".format(err)
		exit(1)


'''
Create user defined tables if it does not exist
'''
def create_table(cursor, table_nm, fields):
	command = "CREATE TABLE IF NOT EXISTS " + table_nm  + " " + fields + " ENGINE=InnoDB"
	cursor.execute(command)


'''
Insert items to user defined tables
'''
def insert_items(con, cursor, table_nm, fields, types, values):
	command = "INSERT INTO " + table_nm + " " + fields + " VALUES " + types
	print command, values
	cursor.execute(command, values)
	con.commit()


'''
Try to connect to the database.
If database does not exist, create the database.
If administrator user does not exist, create user.
'''
try:
	con = mysql.connector.connect(user=user, password=passwd, host=host,database= db)
	cursor = con.cursor(buffered=True)
except mysql.connector.Error as err:		
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print "Soemthing is wrong with your user name or password"
		exit(1)
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
       		print "Database does not exist! Attempting to create " + db + "...."
		con = mysql.connector.connect(user=user, password=passwd)
		cursor = con.cursor(buffered=True)
		create_db(cursor)
		print "Database " + db + " sucessfully created!"
		con.database = db

create_table(cursor, "`UserAccounts`", "(`first_name` varchar(14) NOT NULL, `last_name` varchar(16) NOT NULL,"
		     "`user_id` varchar (15) NOT NULL, `password` varchar(16) NOT NULL, `email` varchar(50) NOT NULL, PRIMARY KEY(user_id))")

create_table(cursor, "`Inventory`", "(`prod_id` varchar(10) NOT NULL, `prod_name` varchar(20) NOT NULL,`description`"
		     "varchar(50), `price` decimal(9,2) NOT NULL, `in_cart` int NOT NULL DEFAULT 0, PRIMARY KEY(prod_id))")

#insert_st = ("INSERT INTO UserAccounts (first_name, last_name, user_id, password, email) VALUES (%s,%s,%s,%s,%s)")
#data = ('Darren', 'Cunningham', '123dr', 'oassw','awd@gmai.com')
#cursor.execute(insert_st, data)
#con.commit()

insert_items(con, cursor, "UserAccounts", "(first_name, last_name, user_id, password, email)", "(%s,%s,%s,%s,%s)", ('Darren', 'Cunningham'
			  , '1232ad', 'pass', 'ois@gmail.com'))
		
insert_items(con, cursor, "Inventory","(prod_id, prod_name, description, price, in_cart)","(%s,%s,%s,%s,%s)",('1239239CR', 'ServerT', 'Server Tower'
		     , '10.95', ''))

insert_items(con, cursor, "`Inventory`","(`prod_id`,`prod_name`,`description`,`price`,`in_cart`)","(%s,%s,%s,%s,%s)",('12459JR','Router','A Mega Awesome Router'
		     , 2000.00,''))

insert_items(con, cursor, "`Inventory`","(`prod_id`,`prod_name`,`description`,`price`,`in_cart`)","(%s,%s,%s,%s,%s)",('87890CR','Firewall',
			  'The most epic Firewall you will ever buy', 10000.00,''))

insert_items(con, cursor, "`Inventory`","(`prod_id`,`prod_name`,`description`,`price`,`in_cart`)","(%s,%s,%s,%s,%s)",('KO2304','IDS/IPS',"'Intrusion" 
		     "Detection System/Intrusion Prevention System'", 980.00,''))

insert_items(con, cursor, "`Inventory`","(`prod_id`,`prod_name`,`description`,`price`,`in_cart`)","(%s,%s,%s,%s,%s)",('99233KOP','VPN','Virtual Private Network'
		     , 5.99,''))

insert_items(con, cursor, "`Inventory`","(`prod_id`,`prod_name`,`description`,`price`,`in_cart`)","(%s,%s,%s,%s,%s)",('KIJ232103','Ethernet Cord','Cat 5 Ethernet Cord'
		     , 2.99,''))

insert_items(con, cursor, "`Inventory`","(`prod_id`,`prod_name`,`description`,`price`,`in_cart`)","(%s,%s,%s,%s,%s)",('OKR12321','AC Plug','Server power cord'
		     , 0.99,''))

insert_items(con, cursor, "`Inventory`","(`prod_id`,`prod_name`,`description`,`price`,`in_cart`)","(%s,%s,%s,%s,%s)",('CH1203','Snickers Bar',
			  'Gotta keep those muscles growing...', 99.99,''))

insert_items(con, cursor, "`Inventory`","(`prod_id`,`prod_name`,`description`,`price`,`in_cart`)","(%s,%s,%s,%s,%s)",('C12345R','Burgers',
			  'Need something random here....', 5.45,''))

cursor.execute("select * from Inventory")

result = cursor.fetchall()

for row in result:
	print row
	
cursor.close()
con.close()	
	
	
