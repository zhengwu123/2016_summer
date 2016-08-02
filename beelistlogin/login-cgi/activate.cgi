#!/python27/ArcGISx6410.2/python.exe
"""
this script use to active the user with primary key email
"""
import cgi,re
import sys, json, urllib, cgi, os, dbmodule_pg, cgitb, psycopg2,random,requests
from email.utils import parseaddr
import cgitb; cgitb.enable() # Optional; for debugging only
from validate_email import validate_email
print "Content-Type: text/html"
print ""

arguments = cgi.FieldStorage()
rawhash = arguments['hash'].value
rawemail = arguments['email'].value
if validate_email(rawemail):
    email = str(arguments['email'].value)
else:
    print "ah?seems somebody modified the email address?"
    exit(1)
if len(rawhash) ==16 and re.match("^[A-Za-z0-9]*$", rawhash):
    hashv = rawhash
else:
    print "u think I am not doing security check, aren't u?"
    exit(1)

try:
    con = dbmodule_pg.getconn()
    cur = con.cursor()
    emailchecksql = "SELECT email FROM lthia.users WHERE email ='%s' AND hashvalue ='%s' AND active = false;" % (email,hashv)
     #check if primary key email already exist in our database?
    cur.execute(emailchecksql)
    con.commit()
    exist = cur.fetchone()
    if exist != None:
        cur.execute("UPDATE lthia.users SET active = true WHERE email = '%s';" % email)
        con.commit()
        print '<script language="javascript">';
        print "alert('Congratulations! account activated,Now you can use your credentials to login.')"
        print 'window.location = "http://beelist.agriculture.purdue.edu/lthia/register.html"';
        print '</script>';
    else:
        print '<script language="javascript">';
        print 'alert("email already actived, or unknown error occured.")';
        print 'window.location = "http://beelist.agriculture.purdue.edu/lthia/register.html"';
        print '</script>';
except psycopg2.DatabaseError, e:
    if con:
        con.rollback()

        print 'Error %s' % e    
        sys.exit(1)
