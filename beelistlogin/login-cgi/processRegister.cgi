#!/python27/ArcGISx6410.2/python.exe
"""
this script use to user register process
"""
print "Content-Type: text/html\n\n";
print "<!DOCTYPE html>";
import sys, json, urllib, cgi, os, dbmodule_pg, cgitb, psycopg2,random,time,fish
import validate_email
import hashlib, uuid # these imports are for encrypt password
import smtplib #module use to send activate email
import smtplib
import requests
from validate_email import validate_email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
#salt = uuid.uuid4().hex
# cgitb use to debug
cgitb.enable()
email = ""
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
#hashvalue is used to actived the user
hashvalue = ''.join(random.choice('0123456789ABCDEF') for i in range(16))

# configuration for sending activation email

sender = 'agriculture.purdue.edu@gmail.com'
receivers = [email]
payload = {'email': email, 'hash': hashvalue}
r = requests.get('http://beelist.agriculture.purdue.edu/cgi-bin/lthia/login/activate.cgi/get', params=payload)
msg = MIMEMultipart('alternative')
msg['Subject'] = "activate Link"
msg['From'] = 'agriculture.purdue.edu@gmail.com'
msg['To'] = 'videobonds@gmail.com'

# Create the body of the message (a plain-text and an HTML version).

html =""" <!DOCTYPE html><html><head><meta charset="UTF-8"><title>Message</title></head><body style="margin:0px; font-family:Tahoma, Geneva, sans-serif;"><div style="padding:10px; background:#ADFF2F; font-size:24px; color:#ffffff;"><a href="#"><img src="http://missouri.agriculture.purdue.edu/logo.png" width="36" height="30" alt="map" style="border:none; float:left;"></a> Account Activation</div><div style="padding:24px; font-size:17px;">Hello user:<br /><br />Click the link below to activate your account:<br /><br /><a href="%s">Click here to activate your account now</a><br /><br />Login after successful activation using your:<br /> E-mail Address: <b>%s</b></div></body></html>
""" % (r.url,email)

# Record the MIME types of both parts - text/plain and text/html.

part1 = MIMEText(html, 'html')

# Attach parts into message container.
# According to RFC 2046, the last part of a multipart message, in this case
# the HTML message, is best and preferred.

msg.attach(part1)

# case for registration
if "register-submit" in formData:
    try:
        con = dbmodule_pg.getconn()
        cur = con.cursor()
        emailchecksql = "SELECT email FROM lthia.users WHERE email ='%s';" % email
            #check if primary key email already exist in our database?
        cur.execute(emailchecksql)
        con.commit()
        exist = cur.fetchone()
        if exist == None:
            cur.execute("INSERT INTO lthia.users (password,email,hashvalue) VALUES ('%s','%s','%s');" % (hashed_password, email, hashvalue))
            con.commit()
            try:
            #send email for user to activate account
                server = smtplib.SMTP('smtp.gmail.com:587')
                server.ehlo()
                server.starttls()
                server.login('agriculture.purdue.edu@gmail.com','Hard2Break')
                server.sendmail(sender, receivers, msg.as_string())         
            except smtplib.SMTPException:
                print "Error: unable to send email"
            print '<script language="javascript">';
            print "alert('registry successful, please check your email box to activate your account')"
            print 'window.location = "http://missouri.agriculture.purdue.edu/register.html"';
            print '</script>';
        else:
            print '<script language="javascript">';
            print 'alert("email already registered,redirecting to login page.")';
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

 
