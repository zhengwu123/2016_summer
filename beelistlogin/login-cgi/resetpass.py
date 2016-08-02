#!/python27/ArcGISx6410.2/python.exe
"""
this script use to user login process
"""
print "Content-Type: text/html\n\n";
print "<!DOCTYPE html>";
import sys, json, urllib, cgi, os, dbmodule_pg, cgitb, psycopg2,random,requests,time,fish
import hashlib, uuid # these imports are for encrypt password
import smtplib #module use to send activate email
import datetime
import smtplib
import requests
# cgitb use to debug
cgitb.enable()

formData = cgi.FieldStorage()
email = formData.getvalue('email')
oldpass = formData.getvalue('pwd0')
newpass = formData.getvalue('pwd1')

if "submit" in formData:
    print '<script language="javascript">';
    print "alert('Can I farking get here?')";
    print '</script>';
    try:
        print '<script language="javascript">';
        print "alert('Am I farking get here?');"
        print '</script>';
        con = dbmodule_pg.getconn()
        cur = con.cursor()
        loginsql = "SELECT email FROM lthia.users WHERE email ='%s' AND password ='%s' AND active =TRUE;" % (email,oldpass)
            #check if primary key email and password combination already exist in our database?
        cur.execute(loginsql)
        con.commit()
        exist = cur.fetchone()
        if exist == None:
            print '<script language="javascript">';
            print "alert('Invalid information.')"
            print 'window.location = "http://beelist.agriculture.purdue.edu/lthia/register.html"';
            print '</script>';
        else:
            #reset password
            resetsql = "UPDATE lthia.users SET password = '%s' WHERE email = '%s';" % (newpass,email)
            cur.execute(resultsql)
            con.commit()
            print '<script language="javascript">';
            print "alert('Password update successful, please log in with your new password.')"
            print 'window.location = "http://beelist.agriculture.purdue.edu/lthia/register.html"';
            print '</script>';
    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()

        print 'Error %s' % e    
        sys.exit(1)
        
    finally:
        if con:
            con.close()
