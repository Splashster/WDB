#!/usr/bin/python

import cgi
import cgitb; cgitb.enable()
import requests
import xml.etree.ElementTree as ET
from lxml import etree
import json

cgi.FieldStorage
form_items = cgi.FieldStorage()
auth_checkbox = form_items.getvalue('auth_search')
title_checkbox = form_items.getvalue('title_con')
type_checkbox = form_items.getvalue('type_search')
abstract_checkbox = form_items.getvalue('abs_con')
author = form_items.getvalue('authorname')
title_content = form_items.getvalue('title_content')
search_type = form_items.getvalue('searchtype')
abstract_content = form_items.getvalue('abstract_content')
responses = []
publication_to_refnum = {'Journal Article':'0', 'Book':'1', 'In a conference proceedings':'3', 'In a collection (part of a book but has its own title)':'5','Tech Report':'10', 'Unpublished':'13', 'Miscellaneous':'16','In a conference proceedings':'47'}
#auth_checkbox = "on"
#author = "W Cui"
#abstract_checkbox = "on"
#abstract_content = "In this paper,"
#type_checkbox = "on"
#search_type = "Journal Article"
main_list = []
baseXMessage = ""
existDBMessage = ""
query_results = ""

refnum_to_publication = {'0': 'Journal Article', '1': 'Book', '3': 'In a conference proceedings', '5': 'In a collection (part of a book but has its own title)', '10': 'Tech Report', '13': 'Unpublished', '16': 'Miscellaneous', '47': 'In a conference proceedings'}
publication_type_list = []

'''
Get all publication types from existdb document.
'''
existdb_response = requests.get('http://localhost:8080/exist/rest/db/acm-turing-awards/acm-turing-awards.xml?_query=distinct-values(//XML/RECORDS/RECORD/REFERENCE_TYPE)&_howmany=1000')


'''
Removing exist result tags that existdb sends back in response.
'''
existdb_pub_types = existdb_response.text.replace('<exist:value exist:type="xs:untypedAtomic">', "").replace('</exist:value>',"").split(">")
existdb_pub_types  = existdb_pub_types[1].split("<")
existdb_pub_types = existdb_pub_types[0].strip().replace("\n", ";").replace(" ", "").split(";")


for existdb_pub_type in existdb_pub_types:
	publication_type_list.append(refnum_to_publication[existdb_pub_type])


'''
Get all publication types from basex document.
'''
basex_response = requests.get('http://admin:admin@localhost:8984/rest/medsamp2012?query=distinct-values(data(//MedlineCitationSet//MedlineCitation//Article//PublicationTypeList//PublicationType))')

for basex_pub_type in basex_response.text.split("\n"):
	publication_type_list.append(str(basex_pub_type))

publication_type_list = list(set(publication_type_list))

'''
Create dropdown elements for each publication types.
All Duplicate publication types have been removed.
'''
options = " "
for i in sorted(publication_type_list):
	options += """<option value="%s">%s</option>\n"""%(i,i)


def parseResponse(response, response_type):
	auth_list = []
	types_list = []
	title = ""
	abs_list = []
	parts_list = []
	main_list = []
	count = 0
	item_count = 1 
	parser = etree.XMLParser(recover=True)

	if response_type == 'baseX':
		tree = "<root>" + response.text + "</root>"
		tree = etree.fromstring(tree,parser)
		root = ET.fromstring(etree.tostring(tree))
		global baseXMessage 
		for child in root.findall("Article"):
			try:
				for i in child.find("PublicationTypeList"):
					try:
						types_list.append(i.text)
					except:
						pass
			except:
				types_list.append("NONE")
		
			try:
				for i in child.find("AuthorList"):
					fullname = i.find("ForeName").text + " " +  i.find("LastName").text
					auth_list.append(fullname)
			except:
				auth_list.append("NONE")
			
			try:
				title = child.find("ArticleTitle").text
			except:
				title = "NONE"
			try:
				if child.findall("Abstract"):
					for i in child.findall("Abstract"):
						try:
							abs_list.append(i.find("AbstractText").text)
						#print abs_list
						except:
							pass
				else:
					 abs_list.append("NONE")
			except:
				abs_list.append("NONE")
		
				
			parts_list.append(types_list)
			parts_list.append(auth_list)
			parts_list.append(title)
			parts_list.append(abs_list)
			main_list.append(parts_list)
			auth_list = []
			types_list = []
			title = ""
			abs_list = []
			parts_list = []
		

		for item in main_list:
			for parts in item:
				if count == 0:
					for i in parts:
						baseXMessage += 'ReferenceType: {0}<br>'.format(i.encode('utf-8'))
					count = 1
				elif count == 1:
					temp = []
					for i in parts:
						temp.append(i.encode('utf-8'))
					authors = ', '.join(temp)
					baseXMessage += 'Authors: ' 
					baseXMessage += '{0} '.format(authors)
					temp = []
					count = 2
					baseXMessage += "<br>"
				elif count == 2:
					baseXMessage += 'Title: {0}<br>'.format(parts.encode('utf-8'))
					count = 3
				elif count == 3:
					for i in parts:
						baseXMessage += 'Abstract: {0}<br>'.format(i.encode('utf-8'))
					count = 0
			if len(main_list) > 1 and item_count < len(main_list):
				baseXMessage+='*********************************************<br>'
				item_count +=1
		main_list = ""
		#print baseXMessage
	else:
		tree = response.text
		tree = etree.fromstring(tree,parser)
		root = ET.fromstring(etree.tostring(tree))
		global existDBMessage 
		for child in root.findall("RECORD"):
			try:
				search_type = refnum_to_publication.get(child.find("REFERENCE_TYPE").text) 
				
				types_list.append(search_type)
			except:
				types_list.append("NONE")
		
			try:
				auth_list.append(child.find(".AUTHORS/AUTHOR").text)
			except:
				auth_list.append("NONE")
			
			try:
				title = child.find("TITLE").text
				#print title_list
			except:
				title = "NONE"
			try:
				abs_list.append(child.find("ABSTRACT").text)
			except:
				abs_list.append("NONE")
			
			parts_list.append(types_list)
			parts_list.append(auth_list)
			parts_list.append(title)
			parts_list.append(abs_list)
			main_list.append(parts_list)
			auth_list = []
			types_list = []
			title = ""
			abs_list = []
			parts_list = []
		count = 0
		for item in main_list:
			for parts in item:
				if count == 0:
					for i in parts:
						existDBMessage += 'ReferenceType: {0}<br>'.format(i)
					count = 1
				elif count == 1:
					temp = []
					for i in parts:
						temp.append(i.encode('utf-8'))
					existDBMessage += 'Authors: ' 
					authors = ', '.join(temp)
					existDBMessage += '{0} '.format(authors)
					temp = []
					count = 2
					existDBMessage += '<br>' 
				elif count == 2:
					existDBMessage += 'Title: {0}<br>'.format(parts.encode('utf-8'))
					count = 3
				elif count == 3:
					for i in parts:
						existDBMessage += 'Abstract: {0}<br>'.format(i.encode('utf-8'))
					count = 0
			if len(main_list) > 1 and item_count < len(main_list):
				existDBMessage+='*********************************************<br>'
				item_count +=1

		#print existDBMessage
		main_list = ""
	#print main_list
	#print existDBMessage

def sendQuery(query, response_type):
	response = requests.get(query)
	if response_type == 'baseX':
		if response.text != "":
			parseResponse(response, response_type)
		else:
			global baseXMessage 
			baseXMessage = "NONE"
	else:
		if ' exist:hits="0" 'not in response.text:
			parseResponse(response, response_type)
		else:
			global existDBMessage
			existDBMessage = "NONE"
def generateBaseXQuery():
	
	xpath = 'MedlineCitationSet/MedlineCitation/Article['
	
	oneChecked = False
	if auth_checkbox:
		try:
			name = author
			fullname = name.split()
			if len(fullname) == 3:
				forename = fullname[0] + " " + fullname[1]
				lastname = fullname[2]
			elif len(fullname) == 2:
				forename = fullname[0]
				lastname = fullname[1]
			elif len(fullname) == 1:
				forename = fullname[0]
				lastname = ""
		except:
			forename = ""
			lastname = ""

		oneChecked = True
		xpath += "AuthorList/Author[LastName= '{0}' and ForeName='{1}']".format(lastname,forename)
	if title_checkbox:
		if oneChecked:
			xpath += " and contains(ArticleTitle,'{0}')".format(title_content)
		else:
			oneChecked = True
			xpath += "contains(ArticleTitle,'{0}')".format(title_content)
	if type_checkbox:
		if oneChecked:
			xpath += " and PublicationTypeList[PublicationType='{0}']".format(search_type)
		else:
			oneChecked = True
			xpath += "PublicationTypeList[PublicationType='{0}']".format(search_type)
	if abstract_checkbox:
		if oneChecked:
			xpath += " and contains(Abstract,'{0}')".format(abstract_content)
		else:
			oneChecked = True
			xpath += "contains(Abstract,'{0}')".format(abstract_content)
	
	if oneChecked: 
		xpath += "]"
		query = 'http://admin:admin@localhost:8984/rest/medsamp2012?query='+xpath+''
		sendQuery(query, 'baseX')
	else:
		global baseXMessage 
		baseXMessage = "NONE"		

def generateExistDBQuery():
	
	xpath = '//XML/RECORDS//RECORD['
	
	oneChecked = False
	if auth_checkbox:

		oneChecked = True
		xpath += "AUTHORS[AUTHOR= '{0}']".format(author)
	if title_checkbox:
		if oneChecked:
			xpath += " and contains(TITLE,'{0}')".format(title_content)
		else:
			oneChecked = True
			xpath += "contains(TITLE,'{0}')".format(title_content)
	if type_checkbox:
		ref_val = publication_to_refnum.get(search_type) 
		if oneChecked:
			xpath += " and REFERENCE_TYPE='{0}'".format(ref_val)
		else:
			oneChecked = True
			xpath += "REFERENCE_TYPE='{0}'".format(ref_val)
	if abstract_checkbox:
		if oneChecked:
			xpath += " and contains(ABSTRACT,'{0}')".format(abstract_content)
		else:
			oneChecked = True
			xpath += "contains(ABSTRACT,'{0}')".format(abstract_content)
	
	if oneChecked: 
		xpath += "]"
		#xpath += '/REFERENCE_TYPE|' + xpath + '/AUTHORS|' + xpath + '/TITLE|' + xpath + '/ABSTRACT'  	
		query = 'http://admin:coursework@localhost:8080/exist/rest/db/acm-turing-awards?_query='+xpath+'&_howmany=10000'
		sendQuery(query, 'existDB')
	else:
		global existDBMessage 
		existDBMessage = "NONE"		
	#print query
generateBaseXQuery()
generateExistDBQuery()
if baseXMessage != "NONE" and existDBMessage != "NONE":
	query_results = baseXMessage + '*********************************************<br>' + existDBMessage
elif baseXMessage == "NONE" and existDBMessage != "NONE":
	query_results = existDBMessage
elif baseXMessage != "NONE" and existDBMessage == "NONE":
	query_results = baseXMessage
else:
	query_results = "NONE"


results_box = json.dumps( "Query Results: \n\n" + query_results.replace("<br>","\n"))

print """ Cotent-type:text/html\r\n\r\n
<html>
<body>
<form action='http://localhost/~coursework/cgi-bin/bibfinder2.cgi' method='post'>
<fieldset style="width:30%; margin-left:35%;">
<label for="author_check" style="margin-right:10%;">
<input name="auth_search" type="checkbox"> Search by Author
</label>
Author's name: <input name="authorname" value={0} style="margin-left:2%;" type="text"><br> 
<label for="title_con" style="margin-right:12%;">
<input name="title_con" type="checkbox"> Title contains...
</label>
Content: <input name="title_content" style="margin-left:12.2%;" type="text"><br> 
<label for="search_type" style="margin-right:13.5%;">
<input name="type_search" type="checkbox"> Search by type
</label>
Type: <select name="searchtype" style="margin-left:16.8%; width:32.7%;">
<option selected>Select Type</option>
{1}
</select>
<br> 
<label for="abstract_con" style="margin-right:6%;">
<input name="abs_con" type="checkbox"> Abstract contains...
</label>
Content: <input name="abstract_content" style="margin-left:12%;" type="text"><br><br>
<input type="submit" value="Submit" style="margin-left:40%;"><br><br> 
<textarea class="scrollabletextbox" id="results" style="width:100%; height:150px; resize:none;"readonly></textarea>
</fieldset>
</form>
<script>document.getElementById("results").innerHTML = {2};</script>
</body>
</html>
""".format(author,options,results_box)
#print msg
