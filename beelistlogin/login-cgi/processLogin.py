#!/python27/ArcGISx6410.2/python.exe
"""
this script use to user login process
"""
print "Content-Type: text/html\n\n";
print "<!DOCTYPE html>";
import sys, json, urllib, cgi, os, dbmodule_pg, cgitb, psycopg2,random,requests,time,fish
from validate_email import validate_email
import hashlib, uuid # these imports are for encrypt password
import smtplib #module use to send activate email
import smtplib
import requests
# cgitb use to debug
cgitb.enable()

formData = cgi.FieldStorage()
if validate_email(str(formData.getvalue('email'))):
    email = str(formData.getvalue('email'))
else:
    print '<script language="javascript">';
    print 'alert("Invalid email.Now redirecting to login page.")';
    print 'window.location = "http://beelist.agriculture.purdue.edu/lthia/register.html"';
    print '</script>';
password = str(formData.getvalue('password'))
hashed_password = hashlib.md5( fish.salt + password ).hexdigest()

if "login-submit" in formData:
    try:
        con = dbmodule_pg.getconn()
        cur = con.cursor()
        loginsql = "SELECT email FROM lthia.users WHERE email ='%s' AND password ='%s' AND active =TRUE;" % (email,hashed_password)
            #check if primary key email and password combination already exist in our database?
        cur.execute(loginsql)
        con.commit()
        exist = cur.fetchone()
        print "%s" % exist
        if exist == None:
            print '<script language="javascript">';
            print "alert('Invalid login information.')"
            print 'window.location = "http://beelist.agriculture.purdue.edu/lthia/register.html"';
            print '</script>';
        else:
            #fetch all table timestamp that created by this user.
            resultsql = "SELECT createdtime FROM lthia.results WHERE login_p ='%s' AND bmpclass = 'Initial' ;" % (email)
            cur.execute(resultsql)
            con.commit()
            rows = cur.fetchall()
            timestamps=[]
            i = 0
            for row in rows:
                timestamps[i] = row
                i+=1
            
            print '<script language="javascript">';
            print 'sessionStorage.setItem("email","'+email+ '");'
            print 'sessionStorage.setItem("timestamps",JSON.stringify(timestamps));'
            print 'window.location = "http://beelist.agriculture.purdue.edu/lthia/index.html"';
            print '</script>';
    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()

        print 'Error %s' % e    
        sys.exit(1)
        
    finally:
        if con:
            con.close()