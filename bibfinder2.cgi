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
main_list = []
baseXResults = ""
existDBResults = ""
query_results = ""
options = ""
refnum_to_publication = {'0': 'Journal Article', '1': 'Book', '3': 'In a conference proceedings', '5': 'In a collection (part of a book but has its own title)', '10': 'Tech Report', '13': 'Unpublished', '16': 'Miscellaneous', '47': 'In a conference proceedings'}


'''
Get all publication types from existdb and baseX documents.
'''

def generateTypesList():
	global options
	publication_type_list = []
	
	'''
	Get existdb publication types
	'''
	existdb_response = requests.get('http://localhost:8080/exist/rest/db/acm-turing-awards/acm-turing-awards.xml?_query=distinct-values(//XML/RECORDS/RECORD/REFERENCE_TYPE)&_howmany=1000')
	existdb_pub_types = existdb_response.text.replace('<exist:value exist:type="xs:untypedAtomic">', "").replace('</exist:value>',"").split(">")
	existdb_pub_types  = existdb_pub_types[1].split("<")
	existdb_pub_types = existdb_pub_types[0].strip().replace("\n", ";").replace(" ", "").split(";")


	for existdb_pub_type in existdb_pub_types:
		publication_type_list.append(refnum_to_publication[existdb_pub_type])


	'''
	Get baseX publication types
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
		if i == search_type: 
			options += """<option value="%s" selected>%s</option>\n"""%(i,i)
		else:
			options += """<option value="%s">%s</option>\n"""%(i,i)


'''
Parses results returned from query.
Generates a compiled list of the results.
'''
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
		global baseXResults 
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
						baseXResults += 'ReferenceType: {0}<br>'.format(i.encode('utf-8'))
					count = 1
				elif count == 1:
					temp = []
					for i in parts:
						temp.append(i.encode('utf-8'))
					authors = ', '.join(temp)
					baseXResults += 'Authors: ' 
					baseXResults += '{0} '.format(authors)
					temp = []
					count = 2
					baseXResults += "<br>"
				elif count == 2:
					baseXResults += 'Title: {0}<br>'.format(parts.encode('utf-8'))
					count = 3
				elif count == 3:
					for i in parts:
						baseXResults += 'Abstract: {0}<br>'.format(i.encode('utf-8'))
					count = 0
			if len(main_list) > 1 and item_count < len(main_list):
				baseXResults+='*********************************************<br>'
				item_count +=1
		main_list = ""
	else:
		tree = response.text
		tree = etree.fromstring(tree,parser)
		root = ET.fromstring(etree.tostring(tree))
		global existDBResults 
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
						existDBResults += 'ReferenceType: {0}<br>'.format(i)
					count = 1
				elif count == 1:
					temp = []
					for i in parts:
						temp.append(i.encode('utf-8'))
					existDBResults += 'Authors: ' 
					authors = ', '.join(temp)
					existDBResults += '{0} '.format(authors)
					temp = []
					count = 2
					existDBResults += '<br>' 
				elif count == 2:
					existDBResults += 'Title: {0}<br>'.format(parts.encode('utf-8'))
					count = 3
				elif count == 3:
					for i in parts:
						existDBResults += 'Abstract: {0}<br>'.format(i.encode('utf-8'))
					count = 0
			if len(main_list) > 1 and item_count < len(main_list):
				existDBResults+='*********************************************<br>'
				item_count +=1

		main_list = ""

def sendQuery(query, response_type):
	response = requests.get(query)
	if response_type == 'baseX':
		if response.text != "":
			parseResponse(response, response_type)
		else:
			global baseXResults 
			baseXResults = "NONE"
	else:
		if ' exist:hits="0" 'not in response.text:
			parseResponse(response, response_type)
		else:
			global existDBResults
			existDBResults = "NONE"

'''
Gerenates baseX query based on user input
'''
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
			xpath += " and contains(lower-case(ArticleTitle),lower-case('{0}'))".format(title_content)
		else:
			oneChecked = True
			xpath += "contains(lower-case(ArticleTitle),lower-case('{0}'))".format(title_content)
	if type_checkbox:
		if oneChecked:
			xpath += " and PublicationTypeList[PublicationType='{0}']".format(search_type)
		else:
			oneChecked = True
			xpath += "PublicationTypeList[PublicationType='{0}']".format(search_type)
	if abstract_checkbox:
		if oneChecked:
			xpath += " and contains(lower-case(Abstract),lower-case('{0}'))".format(abstract_content)
		else:
			oneChecked = True
			xpath += "contains(lower-case(Abstract),lower-case('{0}'))".format(abstract_content)
	
	if oneChecked: 
		xpath += "]"
		query = 'http://admin:admin@localhost:8984/rest/medsamp2012?query='+xpath+''
		sendQuery(query, 'baseX')
	else:
		global baseXResults 
		baseXResults = "NONE"		

'''
Generates existdb query based on user input 
'''
def generateExistDBQuery():
	
	xpath = '//XML/RECORDS//RECORD['
	
	oneChecked = False
	if auth_checkbox:

		oneChecked = True
		xpath += "AUTHORS[AUTHOR= '{0}']".format(author)
	if title_checkbox:
		if oneChecked:
			xpath += " and contains(lower-case(TITLE),lower-case('{0}'))".format(title_content)
		else:
			oneChecked = True
			xpath += "contains(lower-case(TITLE),lower-case('{0}'))".format(title_content)
	if type_checkbox:
		ref_val = publication_to_refnum.get(search_type) 
		if oneChecked:
			xpath += " and REFERENCE_TYPE='{0}'".format(ref_val)
		else:
			oneChecked = True
			xpath += "REFERENCE_TYPE='{0}'".format(ref_val)
	if abstract_checkbox:
		if oneChecked:
			xpath += " and contains(lower-case(ABSTRACT),lower-case('{0}'))".format(abstract_content)
		else:
			oneChecked = True
			xpath += "contains(lower-case(ABSTRACT),lower-case('{0}'))".format(abstract_content)
	
	if oneChecked: 
		xpath += "]"
		query = 'http://admin:coursework@localhost:8080/exist/rest/db/acm-turing-awards?_query='+xpath+'&_howmany=10000'
		sendQuery(query, 'existDB')
	else:
		global existDBResults 
		existDBResults = "NONE"		

'''
Generates combined result list from the baseX and existdb query results.
If the baseX and existdb both returned nothing, NONE will be the only
item in the result list.
'''
def generateFinalResults():
	global query_results
	if baseXResults != "NONE" and existDBResults != "NONE":
		query_results = baseXResults + '*********************************************<br>' + existDBResults
	elif baseXResults == "NONE" and existDBResults != "NONE":
		query_results = existDBResults
	elif baseXResults != "NONE" and existDBResults == "NONE":
		query_results = baseXResults
	else:
		query_results = "NONE"

	query_results = json.dumps( "Query Results: \n\n" + query_results.replace("<br>","\n"))


generateTypesList()
generateBaseXQuery()
generateExistDBQuery()
generateFinalResults()

if json.dumps(author) == "null":
	author = ""
else:
	author = json.dumps(author)
if json.dumps(title_content) == "null":
	title_content = ""
else:
	title_content = json.dumps(title_content)
if json.dumps(abstract_content) == "null":
	abstract_content = ""

if auth_checkbox:
	auth_checkbox = "checked"
else:
	auth_checkbox = ""
if title_checkbox:
	title_checkbox = "checked"
else:
	title_checkbox = ""
if type_checkbox:
	type_checkbox = "checked"
else:
	type_checkbox = ""
if abstract_checkbox:
	abstract_checkbox = "checked"
else:
	abstract_checkbox = ""

print """ Cotent-type:text/html\r\n\r\n
<html>
<body>
<div style="text-align:center;">
<form action='http://localhost/~coursework/cgi-bin/bibfinder2.cgi' method='post'>
<fieldset style="display:inline-block;text-align:left;">
<label for="author_check" style="padding-right:18.2%;">
<input name="auth_search" type="checkbox" {0}> Search by Author
</label>
Author's name: <input name="authorname" type="text" value={1}><br> 
<label for="title_con" style="padding-right:20.5%;">
<input name="title_con" type="checkbox" {2}> Title contains...
</label>
Content: <input name="title_content" style="margin-left:9%;" type="text" value={3}><br> 
<label for="search_type" style="padding-right:22%;">
<input name="type_search" type="checkbox" {4}> Search by type
</label>
Type: <select name="searchtype" style="margin-left:13.3%; width:30.6%;">
<option>Select Type</option>
{5}
</select>
<br> 
<label for="abstract_con" style="padding-right:15%;">
<input name="abs_con" type="checkbox" {6}> Abstract contains...
</label>
Content: <input name="abstract_content" style="margin-left:8.8%;" type="text" value={7}><br><br>
<input type="submit" value="Submit" style="margin-left:40%;"><br><br> 
<textarea class="scrollabletextbox" id="results" style="width:100%; height:150px; resize:none;"readonly></textarea>
</fieldset>
</form>
</div>
<script>document.getElementById("results").innerHTML = {8};</script>
</body>
</html>
""".format(auth_checkbox,author,title_checkbox,title_content,type_checkbox,options,abstract_checkbox,abstract_content,query_results)
