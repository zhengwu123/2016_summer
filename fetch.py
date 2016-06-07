#!/usr/local/bin/python
import urllib, json, sys, cgi,cgitb
url = "http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50&outputFormat=application%2Fjson&CQL_FILTER=STATE_NAME='Indiana'%20OR%20STATE_NAME='Michigan'"
response = urllib.urlopen(url)
data = json.loads(response.read())
#print data
myjson =json.load(sys.stdin)
print response
