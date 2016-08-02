#!/python27/ArcGISx6410.2/python.exe
"""
this script use to active the user with primary key email
"""
import cgi,re
import sys, json, urllib, cgi, os, dbmodule_pg, cgitb, psycopg2,random,requests,fish
from email.utils import parseaddr
import cgitb; cgitb.enable() # Optional; for debugging only
from validate_email import validate_email
import smtplib
import requests
import hashlib, uuid # these imports are for encrypt password
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
tempass = ''.join(random.choice('0123456789ABCDEF') for i in range(16))
hashed_password = hashlib.md5( fish.salt + tempass ).hexdigest()
formData = cgi.FieldStorage()
if validate_email(str(formData.getvalue("email"))):
    email = str(formData.getvalue('email'))
    print "Content-Type: text/html"     # HTML is following
    print                               # blank line, end of headers

    print

    print(email)
    # configuration for sending temporary email

    sender = 'agriculture.purdue.edu@gmail.com'
    receivers = [email]
    msg = MIMEMultipart('alternative')
    msg['Subject'] = "temporary password"
    msg['From'] = 'agriculture.purdue.edu@gmail.com'
    msg['To'] = 'videobonds@gmail.com'

    # Create the body of the message (a plain-text and an HTML version).

    html =""" <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Message</title></head><body style="margin:0px; font-family:Tahoma, Geneva, sans-serif;"><div style="padding:10px; background:#ADFF2F; font-size:24px; color:#ffffff;"><a href="#"><img src="http://missouri.agriculture.purdue.edu/logo.png" width="36" height="30" alt="map" style="border:none; float:left;"></a> Temporary password </div><div style="padding:24px; font-size:17px;">Hello user:<br /><br />Copy the password below to log into your account:<br /><br /><strong> "%s"</strong><br /><br />Login using your:<br /> E-mail Address: <b>%s</b></div></body></html>
    """ % (tempass,email)

    # Record the MIME types of both parts - text/plain and text/html.

    part1 = MIMEText(html, 'html')

    msg.attach(part1)
    try:
        con = dbmodule_pg.getconn()
        cur = con.cursor()
        emailchecksql = "SELECT email FROM lthia.users WHERE email ='%s';" % email
            #check if primary key email already exist in our database?
        cur.execute(emailchecksql)
        con.commit()
        exist = cur.fetchone()
        if exist == None:
            print '<script language="javascript">';
            print 'alert("Invalid email.")';
            print 'window.location = "http://beelist.agriculture.purdue.edu/lthia/register.html"';
            print '</script>';
            
        else:
            try:
            #send temporary password email
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login('agriculture.purdue.edu@gmail.com','Hard2Break')
                server.sendmail(sender, receivers, msg.as_string())
                #update password
                cur.execute("UPDATE lthia.users SET password = '%s' WHERE email = '%s';" % (hashed_password, email))
                con.commit()
            except smtplib.SMTPException:
                print "Error: unable to send email"
            
            print '<script language="javascript">';
            print "alert('Please check your email box for your temporary password')"
            print 'window.location = "http://beelist.agriculture.purdue.edu/lthia/register.html"';
            print '</script>';
    except psycopg2.DatabaseError, e:
        if con:
            con.rollback()
else:
    print "invalid email address."
