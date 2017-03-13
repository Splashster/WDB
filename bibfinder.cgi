#!/usr/bin/python
import cgi
import requests


publication_type_mapping = {'0': 'Journal Article', '1': 'Book', '3': 'In a conference proceedings', '5': 'In a collection (part of a book but has its own title)', '10': 'Tech Report', '13': 'Unpublished', '16': 'Miscellaneous', '47': 'In a conference proceedings'}
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
	publication_type_list.append(publication_type_mapping[existdb_pub_type])


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

print """ Cotent-type:text/html\r\n\r\n
<html>
<body>
<div style="text-align:center;">
<form action='http://localhost/~coursework/cgi-bin/bibfinder2.cgi' method='post'>
<fieldset style="display:inline-block;text-align:left;">
<label for="author_check" style="padding-right:18.2%;">
<input name="auth_search" type="checkbox"> Search by Author
</label>
Author's name: <input name="authorname" type="text"><br> 
<label for="title_con" style="padding-right:20.5%;">
<input name="title_con" type="checkbox"> Title contains...
</label>
Content: <input name="title_content" style="margin-left:9%;" type="text"><br> 
<label for="search_type" style="padding-right:22%;">
<input name="type_search" type="checkbox"> Search by type
</label>
Type: <select name="searchtype" style="margin-left:13.3%; width:30.6%;">
<option>Select Type</option>
{0}
</select>
<br> 
<label for="abstract_con" style="padding-right:15%;">
<input name="abs_con" type="checkbox"> Abstract contains...
</label>
Content: <input name="abstract_content" style="margin-left:8.8%;" type="text"><br><br>
<input type="submit" value="Submit" style="margin-left:40%;"><br><br> 
<textarea class="scrollabletextbox" id="results" style="width:100%; height:150px; resize:none;"readonly></textarea>
</fieldset>
</form>
</div>
</body>
</html>
""".format(options)

