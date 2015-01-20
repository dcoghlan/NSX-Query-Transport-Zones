#
# Script to get NSX Transport Zones
 
import requests
import sys
from xml.dom import minidom

#
# Module to help display XML correctly
from xml.dom.minidom import parse, parseString

#
# Sets a variable to save the HTTP/XML reponse so it can be parsed and displayed.
_responsefile = 'xml-transport-zones.xml'

#
# If there aren't enough arguments when the script is called, then display a message and exit.
if len(sys.argv) != 4:
 print (len(sys.argv))
 print ("Usage: python nsx-query-tz.py username password nsx_manager_hostname")
 sys.exit()

#
# Reads command line arguments and saves them to variables
_user = sys.argv[1]
_password = sys.argv[2]
_nsxmgr = sys.argv[3]

# Sets the formatting for the columns
_outputHeader = '{0:12} {1:25} {2:16} {3:50}'
_outputBody = '{0:12} {1:25} {2:16} {3:50}'

#
# Set the application content-type header value
myheaders = {'Content-Type': 'application/xml'}

#
# NSX API URL to get the Transport Zones
requests_url = 'https://%s/api/2.0/vdn/scopes' % (_nsxmgr)

#
# Submits the request to the NSX Manager
success = requests.get((requests_url), headers=myheaders, auth=(_user, _password), verify=False)
_data=success.content

#
# Opens a file for writing and saves the XML response to the file to be parsed further down.
_responsexml = open('%s' % _responsefile, 'w+')
_responsexml.write(success.text);

#
# Close the XML response file
_responsexml.close()

#
# (DEBUGGING) Uncomment all this section to display the xml response file from above in a pretty format on the screen
#_responsexml = open('%s' % _responsefile, 'r+')
#_dom4 = parse(_responsexml)
#_responsexml.close()
#print (_dom4.toprettyxml())

# Load the response file into dom
doc = minidom.parse(_responsefile)

vdnScopes = doc.getElementsByTagName("vdnScope")

print(_outputHeader.format("ObjectID", "Name", "Mode", "Description"))
print("-"*80)

for tz in vdnScopes:
	# clears the list
	tzlist = [];
	# Grabs the Object Id and adds it to the list
	oid = tz.getElementsByTagName("objectId")[0]
	tzlist = [(oid.firstChild.data)]
	
	# Grabs the transport zone name and adds to the list
	tzname = tz.getElementsByTagName("name")[0]
	tzlist.append(tzname.firstChild.data);
	
	# Grabs the transport zone control plane mode and adds it to the list
	cpmode = tz.getElementsByTagName("controlPlaneMode")[0]
	tzlist.append(cpmode.firstChild.data);
	
	# Tries to grabs the transport zone description
	tzdescription = tz.getElementsByTagName("description")[0]
	
	# As the description field is not a required field, we need to try and see if there is any data
	# and if there is no data for the description element, then it will thrown an exception and append 
	# a blank value for the description
	try:
		tzlist.append(tzdescription.firstChild.data);
	except:
		tzlist.append("")
	
	print(_outputBody.format(tzlist[0], tzlist[1], tzlist[2], tzlist[3]))

exit()
