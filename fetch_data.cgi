#!/usr/local/bin/python
#import urllib, json, sys,cgi,cgitb
#url = "http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50&outputFormat=application%2Fjson&CQL_FILTER=STATE_NAME='Indiana'%20OR%20STATE_NAME='Michigan'"
#response = urllib.urlopen(url)
#data = json.loads(response.read())
#print data
#print data
import sys, json, urllib,cgi,os

fs = cgi.FieldStorage()

sys.stdout.write("Content-Type: application/json")

sys.stdout.write("\n")
sys.stdout.write("\n")

#url = "http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50&outputFormat=application%2Fjson&CQL_FILTER=STATE_NAME='Indiana'%20OR%20STATE_NAME='Michigan'"
url = ""
result = {}
result['success'] = True
result['message'] = "The command Completed Successfully"
result['keys'] = ",".join(fs.keys())
a = ""
if 'IN' in fs.keys() and 'MI' not in fs.keys() and 'OH' not in fs.keys():
	a = "IN"
	url = "http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50&outputFormat=application%2Fjson&CQL_FILTER=STATE_NAME='Indiana'"
elif 'MI' in fs.keys() and 'IN' not in fs.keys() and 'OH' not in fs.keys():
	a = "MI"
	url = "http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50&outputFormat=application%2Fjson&CQL_FILTER=STATE_NAME='Michigan'"
elif 'OH' in fs.keys() and 'MI' not in fs.keys() and 'IN' not in fs.keys():
	a = "OH"
	url = "http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50&outputFormat=application%2Fjson&CQL_FILTER=STATE_NAME='Ohio'"
elif 'MI' in fs.keys() and 'IN' in fs.keys() and 'OH' not in fs.keys():
	a = "MI IN"
	url = "http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50&outputFormat=application%2Fjson&CQL_FILTER=STATE_NAME='Indiana'%20OR%20STATE_NAME='Michigan'"
elif 'OH' in fs.keys() and 'MI' in fs.keys() and 'IN' not in fs.keys():
	a = "OH MI"
	url = "http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50&outputFormat=application%2Fjson&CQL_FILTER=STATE_NAME='Ohio'%20OR%20STATE_NAME='Michigan'"
elif 'OH' in fs.keys() and 'IN' in fs.keys() and 'MI' not in fs.keys():
	a = "IN OH"
	url = "http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50&outputFormat=application%2Fjson&CQL_FILTER=STATE_NAME='Indiana'%20OR%20STATE_NAME='Ohio'"
elif 'OH' in fs.keys() and 'MI' in fs.keys() and 'IN' in fs.keys():
	a = "IN OH MI"
	url = "http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50&outputFormat=application%2Fjson&CQL_FILTER=STATE_NAME='Indiana'%20OR%20STATE_NAME='Michigan'%20OR%20STATE_NAME='Ohio'"

response = urllib.urlopen(url)
data = json.loads(response.read())

d = {}
for k in fs.keys():
    d[k] = fs.getvalue(k)
result['data'] = d

sys.stdout.write(json.dumps(data))
sys.stdout.write("\n")

sys.stdout.close()