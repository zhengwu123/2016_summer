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

result = cgi.FieldStorage()
session_id=result.getfirst("session_id")
try:
    con = dbmodule_pg.getconn()
    cur = con.cursor()
    tablesql = "SELECT bmpclass,avgrunoff, avgtotss, avgtotp, avgtotn, avgtotpb, avgtotcu, avgtotzn, avgtotec FROM lthia.results WHERE session_id ='%s';" % (session_id)
     #check if primary key email already exist in our database?
    cur.execute(tablesql)
    con.commit()
    #row = cur.fetchone()
    table = '<table border="1">' 
    table += '<tr><td>BMP</td><td>Runoff Volume(m^3/yr)</td><td>Suspended Sediment (kg/m^2/year)</td><td>Phosphorus (kg/m^2/year)</td><td>Nitrogen (kg/m^2/year)</td><td>Lead (kg/m^2/year)</td><td>Copper (kg/m^2/year)</td><td>Zinc (kg/m^2/year)</td><td>E. Coli (MPN/100mL/m^2/year)</td></tr>'
    rows = cur.fetchall()
    for row in rows:
        if row != None:
            table += '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td <td>%s</td></tr>' % row
        else:
            print '\"unknown error happend.\"'
    print table
except psycopg2.DatabaseError, e:
    if con:
        con.rollback()

        print 'Error %s' % e    
        sys.exit(1)
