#!/Python27/ArcGIS10.2/python.exe

import string, random
import psycopg2
import sqlalchemy.pool as pool
from databasetablenames import * #can change for other states.
from datetime import datetime, timedelta
import hashlib

def getconn():
    """
    Retrieve a connect object with psycopg2 library.
    """
    c = psycopg2.connect(" ".join(['host=localhost', 'user=postgres', 'dbname=postgis', 'password=Hard2Break']))
    # execute an initialization function on the connection before returning # not necessary?
    #c.cursor().execute("setup_encodings()")
    return c

connPool = pool.QueuePool(getconn, max_overflow=10, pool_size=5)

def GetPgConnection():
    """
    Return a connection from the database.
    Return 1 and a connection object if success, otherwise 0 and error message.
    Use sqlachemy connection pool.
    """
    return 1, connPool.unique_connection()

def GetPgCursor():
    """
    Return a database connection cursor for py session.
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        ret2, cur = conn.cursor()
        if ret2 == 1:
            return cur
        else:
            return None
    else:
        return None

def ExecuteSQL(connObj, sqlState):
    """
    An internal function for sql statement execution.
    Return 1 and a success message, otherwise 0 and error message.
    """
    try:
        cursorObj = connObj.cursor()
        cursorObj.execute(sqlState)
        connObj.commit()
        cursorObj.close()
        return 1, 'SQL statement successfully executed!'
    except psycopg2.Error, e:
        cursorObj.rollback()
        return 0, e.args[0]

def DoesSessionIdExist(sessionId, schema=TbNames.Schema, tbname=TbNames.Sessions):
    """
    Check whether a given session id exists in the table sessions.
    Parameter: schema and table name in PostgreSQL database, defaulted
    can be others if needed.
    Return 1 and 1 or 0 if success, otherwise 0 and error message.
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        sql_st = "SELECT session_id FROM \"" + schema +"\".\"" + tbname + "\" WHERE session_id ~ %s;"
        t = (sessionId,)
        try:
            cur = conn.cursor()
            cur.execute(sql_st, t)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            return 1, len(rows)
        except psycopg2.Error, e:
            return 0, 0 # not return string here
    else:
        return 0, 0 # conn


def GetNextId(tbname, schema=TbNames.Schema):
    """
    Retrieve the max gid in a table add one then return.
    Parameter: schema and table name in PostgreSQL database.
    Table name could be that of any table in the database.
    Return 1 and newid if success, otherwise 0 and error message.
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        sql_st = "SELECT MAX(gid) FROM \"%s\".\"%s\";" % (schema, tbname) # schema and table don't need escape
        try:
            cur = conn.cursor()
            cur.execute(sql_st)
            maxid = cur.fetchone()[0]
            if maxid is None: # in case it is an empty table
                maxid = 0
            conn.commit()
            cur.close()
            conn.close()
            return 1, maxid + 1
        except psycopg2.Error, e:
            return 0, e.args[0]
    else:
        return 0, conn
        
def GetNextScenarioId(sessionid, tbname=TbNames.Scenarios, schema=TbNames.Schema):
    """
    Retrieve the max gid in a table add one then return.
    Parameter: schema and table name in PostgreSQL database.
    Table name could be that of any table in the database.
    Return 1 and newid if success, otherwise 0 and error message.
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        sql_st = "SELECT MAX(scenario_num) FROM \"%s\".\"%s\" WHERE session_id = '%s';" % (schema, tbname, sessionid) # schema and table don't need escape
        try:
            cur = conn.cursor()
            cur.execute(sql_st)
            maxid = cur.fetchone()[0]
            if maxid is None: # in case it is an empty table
                maxid = 0
            conn.commit()
            cur.close()
            conn.close()
            return 1, maxid + 1
        except psycopg2.Error, e:
            return 0, e.args[0]
    else:
        return 0, conn

def GetNewSessionId(tbname = TbNames.Sessions, schema = TbNames.Schema):
    """
    Creates a new session id for a new user
    Paramaters: takes a database schema, defaults to the lthia schema
    returns 1 and id on success otherwise 0 and error message
    """
    sql_st = "INSERT INTO \"" + schema + "\".\"" + tbname + "\" (session_id,time_created) \
                VALUES (%s,%s);"
    ret, conn = GetPgConnection()
    if ret == 1:
        try:
            i = 0
            sessionid = ''
            while(i < 16 or DoesSessionIdExist(sessionid)[1]):
                if(i>=16):
                    sessionid = ''
                    i = 0
                j = chr(random.randint(0,127))
                if(j in string.ascii_lowercase or j in string.ascii_uppercase or j in string.digits):
                    sessionid += j
                    i+=1
            creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            cur = conn.cursor()
            cur.execute(sql_st, (sessionid, creation_time,))
            conn.commit()
            cur.close()
            conn.close()
            return 1, sessionid
        except psycopg2.Error, e:
            conn.rollback()
            return 0, e.args[0]
    return sessionid
    
def CreateNewSession(sessionid, tbname = TbNames.Sessions, schema = TbNames.Schema):
    """
    Creates a new session, but requires the user to pass a session id
    Paramaters: takes a database schema, defaults to the lthia schema
    returns 1 and id on success otherwise 0 and error message
    """
    sql_st = "INSERT INTO \"" + schema + "\".\"" + tbname + "\" (session_id,time_created) \
                VALUES (%s,%s);"
    ret, conn = GetPgConnection()
    if ret == 1:
        try:
            i = 0
            creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            if len(sessionid) == 16:
                sessionid = '*' + sessionid
            
            cur = conn.cursor()
            cur.execute(sql_st, (sessionid, creation_time,))
            conn.commit()
            cur.close()
            conn.close()
            return 1, sessionid
        except psycopg2.Error, e:
            conn.rollback()
            return 0, e.args[0]
    return sessionid

# def NewEntry(infos, tbname, schema=TbNames.Schema):
    # """
    # Insert a new record into one of the data tables
    # Parameter: infos is a list of area information, schema and table name in PostgreSQL database, schema defaults to lthia,
    # can be others if they were created in database.
    # Return 1 and successful message, otherwise 0 and error message.
    # """
    # ret, conn = GetPgConnection()
    # if ret == 1:
        # try:
            # latlon = string.split(infos[1],"|")
            # poly = []
            # for xy in latlon:
                # if not (xy == ""):
                    # xyl = string.split(xy, ",")
                    # poly.append(xyl[0] + " " + xyl[1])
            # #repeat the last point to close the polygon or will get the ring not close error
            # poly.append(poly[0])
            # wkt = "POLYGON((" + string.join(poly, ",") + "))"
            # geomText = "GeometryFromText('" + wkt + "', 4326)"
            # gid =GetNextId(tbname,schema)[1]

            # sql_st = "INSERT INTO \"" + schema + "\".\"" + tbname + "\" (gid,session_id,coords,polygon) \
                # VALUES ("+str(gid)+",%s,%s,"+geomText+");"

            # cur = conn.cursor()
            # cur.execute(sql_st, infos)
            # conn.commit()
            # cur.close()
            # conn.close()
            # return gid, "New area created."
        # except psycopg2.Error, e:
            # conn.rollback()
            # return 0, e.args[0]
    # else:
        # return 0, conn
        
def NewEntry(values, tbname, colnames=('session_id','coords',), schema=TbNames.Schema):
    """
    Insert a new record into one of the data tables
    Parameter: values is a list of area information, schema and table name in PostgreSQL database, schema defaults to lthia,
    can be others if they were created in database.
    Return 1 and successful message, otherwise 0 and error message.
    """
    #print "THESE ARE THE VALUES IN NEWENTRY <BR \>"
    #print values
    #print "<BR \>"
    ret, conn = GetPgConnection()
    if ret == 1 and len(colnames) > 0 and len(values) > 0:
        try:
            i = 0
            gid =GetNextId(tbname,schema)[1]
            names = ['gid']
            infos = [str(gid)]
            while i < len(colnames) and i < len(values):
                names += [str(colnames[i])]
                if isinstance(values[i], str):
                    infos += ["'"+values[i]+"'"]
                else:
                    infos += [values[i]]
                if colnames[i] == 'coords':
                    latlon = string.split(values[i],"|")
                    poly = []
                    for xy in latlon:
                        if not (xy == ""):
                            xyl = string.split(xy, ",")
                            poly.append(xyl[0] + " " + xyl[1])
                    #repeat the last point to close the polygon or will get the ring not close error
                    poly.append(poly[0])
                    wkt = "POLYGON((" + string.join(poly, ",") + "))"
                    geomText = "GeometryFromText('" + wkt + "', 4326)"
                    names += ['polygon']
                    infos += [geomText]
                i+=1
            # latlon = string.split(infos[1],"|")
            # poly = []
            # for xy in latlon:
                # if not (xy == ""):
                    # xyl = string.split(xy, ",")
                    # poly.append(xyl[0] + " " + xyl[1])
            #repeat the last point to close the polygon or will get the ring not close error
            # poly.append(poly[0])
            # wkt = "POLYGON((" + string.join(poly, ",") + "))"
            # geomText = "GeometryFromText('" + wkt + "', 4326)"
            

            sql_st = "INSERT INTO \"" + schema + "\".\"" + tbname + "\" ("+','.join(names)+") \
                VALUES ("+','.join(['%s' for x in range(len(infos))])+");"
            # print sql_st
            # print ','.join(infos)

            # print len(infos)
            infos = tuple(infos)
            
            sql_st = sql_st % infos
            
            cur = conn.cursor()
            cur.execute(sql_st, infos)
            conn.commit()
            cur.close()
            conn.close()
            return gid, "New area created."
        except psycopg2.Error, e:
            conn.rollback()
            return 0, e.args[0]
    else:
        return 0, conn

def EditEntry(areaId, infos, tbname, schema=TbNames.Schema):
    """
    Modify a record in one of the data tables
    Parameter: infos is a list of area information, schema and table name in PostgreSQL database, schema defaults to lthia,
    can be others if they were created in database.
    Return 1 and successful message, otherwise 0 and error message.
    """
    ret, conn = GetPgConnection()
    if ret == 1:

        try:
            latlon = string.split(infos[1],"|")
            poly = []
            for xy in latlon:
                if not (xy == ""):
                    xyl = string.split(xy, ",")
                    poly.append(xyl[0] + " " + xyl[1])
            #repeat the last point to close the polygon or will get the ring not close error
            poly.append(poly[0])
            wkt = "POLYGON((" + string.join(poly, ",") + "))"
            geomText = "GeometryFromText('" + wkt + "', 4326)"

            sql_st = 'UPDATE "' + schema + '"."' + tbname + '" \
               SET session_id=%s, coords=%s, polygon='+geomText+' \
               WHERE gid=' + str(areaId)

            cur = conn.cursor()
            cur.execute(sql_st, infos)
            conn.commit()
            cur.close()
            conn.close()
            return 1, "One area modified."
        except psycopg2.Error, e:
            conn.rollback()
            return 0, e.args[0]
    else:
        return 0, conn

def EditProperties(areaId, properties, values, tbname, schema=TbNames.Schema):
    """
    Modify a record in one of the data tables
    Parameter:
        properties is a list of column names in the table
        values is a list of values to set the respective column entries to
        schema and table name in PostgreSQL database, schema defaults to lthia,
            can be others if they were created in database.
    Return 1 and successful message, otherwise 0 and error message.
    """
    ret, conn = GetPgConnection()
    if ret == 1 and len(properties) > 0 and len(values) > 0:

        try:
            i = 0
            num = 0
            names = []
            infos = []
            while i < len(properties) and i < len(values):
                names += [str(properties[i]) + '=%s']
                infos += [values[i]]
                if properties[i] == 'coords':
                    latlon = string.split(values[i],"|")
                    poly = []
                    for xy in latlon:
                        if not (xy == ""):
                            xyl = string.split(xy, ",")
                            poly.append(xyl[0] + " " + xyl[1])
                    #repeat the last point to close the polygon or will get the ring not close error
                    poly.append(poly[0])
                    wkt = "POLYGON((" + string.join(poly, ",") + "))"
                    geomText = "GeometryFromText('" + wkt + "', 4326)"
                    names += ['polygon=%s']
                    infos += [geomText]
                    num+=1
                num+=1
                i+=1

            infos+=[str(areaId)]
            names = tuple(names)

            #create the sql statement with schema and table name
            sql_st = 'UPDATE "' + schema + '"."' + tbname + '" SET %s WHERE gid=%s'

            #populate the SET area with %s=%s, %s=%s, ...
            #extra %s in tuple preserves the gid=%s for the areaId
            #areaId is not added here so the execute function can escape/quote it properly
            sql_st = sql_st % (', '.join(names), '%s',)

            #must be a tuple to insert properly
            infos = tuple(infos)

            cur = conn.cursor()
            cur.execute(sql_st, infos)
            conn.commit()
            cur.close()
            conn.close()
            return 1, "One area modified."
        except psycopg2.Error, e:
            conn.rollback()
            return 0, e.args[0]
    else:
        return 0, conn

def GetScenarioGid(session, scen_num, tbname=TbNames.Scenarios, schema=TbNames.Schema):
    """
    Gets all entries from a database table
    Parameters: table name and schema in the database, schema defaults to lthia
    Return 1 and rows on success, 0 and error on failure
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        sql_st = '''SELECT gid FROM "%s"."%s" WHERE session_id  = '%s' AND scenario_num = '%s';''' % (schema, tbname, session, scen_num)
        try:
            cur = conn.cursor()
            cur.execute(sql_st)
            gid = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            if gid == None:
                return 0, "Scenario not in table"
            return 1, gid
        except psycopg2.Error, e:
            return 0, e.args[0]
    else:
        return 0, conn
        
def GetGidFromSession(session, tbname=TbNames.Watersheds, schema=TbNames.Schema):
    """
    Gets all entries from a database table
    Parameters: table name and schema in the database, schema defaults to lthia
    Return 1 and rows on success, 0 and error on failure
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        sql_st = '''SELECT gid FROM "%s"."%s" WHERE session_id  ~ '%s';''' % (schema, tbname, session)
        try:
            cur = conn.cursor()
            cur.execute(sql_st)
            gid = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            if gid == None:
                return 0, "Session not in table"
            return 1, gid
        except psycopg2.Error, e:
            return 0, e.args[0]
    else:
        return 0, conn

def DeleteByGids(gids, tbname, schema=TbNames.Schema):
    """
    Deletes entries from one of the data tables
    Parameters: areaIds is a list of area gid(s), schema and table name in PostgreSQL database, schema defaults to lthia,
    can be others if they were created in database.
    Return 1 and successful message, otherwise 0 and error message.
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        sql_st = 'DELETE FROM "' + schema + '"."' + tbname + '" WHERE gid IN (%s)'
        t = (",".join(map(str, gids)),)
        try:
            cur = conn.cursor()
            cur.execute(sql_st % t)
            conn.commit()

            cur.close()
            conn.close()
            return 1, "Areas sucessfully deleted."
        except psycopg2.Error, e:
            conn.rollback()
            conn.close()
            return 0, e.args[0]

    else:
        return 0, conn

def DeleteByGid(gid, tbname, schema=TbNames.Schema):
    """
    Deletes entries from one of the data tables
    Parameters: sessionIds is a list of session ids, schema and table name in PostgreSQL database, schema defaults to lthia,
    can be others if they were created in database.
    Return 1 and successful message, otherwise 0 and error message.
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        sql_st = 'DELETE FROM "' + schema + '"."' + tbname + "\" WHERE gid = %s"
        try:
            cur = conn.cursor()
            cur.execute(sql_st % gid)
            conn.commit()

            cur.close()
            conn.close()
            return 1, "Areas sucessfully deleted."
        except psycopg2.Error, e:
            conn.rollback()
            conn.close()
            return 0, e.args[0]

    else:
        return 0, conn

def DeleteById(sessionId, tbname, schema=TbNames.Schema):
    """
    Deletes entries from one of the data tables
    Parameters: sessionIds is a list of session ids, schema and table name in PostgreSQL database, schema defaults to lthia,
    can be others if they were created in database.
    Return 1 and successful message, otherwise 0 and error message.
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        sql_st = 'DELETE FROM "' + schema + '"."' + tbname + "\" WHERE session_id  ~ '%s'"
        try:
            cur = conn.cursor()
            cur.execute(sql_st % sessionId)
            conn.commit()

            cur.close()
            conn.close()
            return 1, "Areas sucessfully deleted."
        except psycopg2.Error, e:
            conn.rollback()
            conn.close()
            return 0, e.args[0]

    else:
        return 0, conn

def DeleteByIds(sessionIds, tbname, schema=TbNames.Schema):
    """
    Deletes entries from one of the data tables
    Parameters: sessionIds is a list of session ids, schema and table name in PostgreSQL database, schema defaults to lthia,
    can be others if they were created in database.
    Return 1 and successful message, otherwise 0 and error message.
    """
    for id in sessionIds:
        DeleteEntryById(id, tbname, schema)

def GetAll(tbname, schema = TbNames.Schema):
    """
    Gets all entries from a database table
    Parameters: table name and schema in the database, schema defaults to lthia
    Return 1 and rows on success, 0 and error on failure
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        sql_st = 'SELECT * FROM "%s"."%s";' % (schema, tbname)
        try:
            cur = conn.cursor()
            cur.execute(sql_st)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            return 1, rows
        except psycopg2.Error, e:
            return 0, e.args[0]
    else:
        return 0, conn

#Made by Matt Lazar
def GetQuery(tbname, column, condition, schema = TbNames.Schema):
    """
    Gets all entries from a database table
    Parameters: table name, column(s) that will be returned, condition that they be returned on, and schema in the database, schema defaults to lthia
    Example: to execute " SELECT name, age FROM "school"."students" WHERE grades = 'A' ",
    set tbname = students, column = "name, age", condition = "grades = "A", and schema = "school"
    Return 1 and rows on success, 0 and error on failure
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        sql_st = 'SELECT %s FROM "%s"."%s" WHERE %s;' % (column, schema, tbname, condition)
        try:
            cur = conn.cursor()
            cur.execute(sql_st)
            rows = cur.fetchall()
            conn.commit()
            cur.close()
            conn.close()
            return 1, rows
        except psycopg2.Error, e:
            return 0, e.args[0]
    else:
        return 0, conn
        
def ScenarioCompatibility(scenType, baseScenario, session, tbname = TbNames.Scenarios, schema = TbNames.Schema):
    """
    compares a new scenarios type to that of its base
    if the new is rast and the old was num, returns false
    else, returns true
    """
    ret, conn = GetPgConnection()
    if ret == 1:
        sql_st = '''SELECT scenario_type FROM "%s"."%s" WHERE (session_id, scenario_num) = ('%s',%d);''' % (schema, tbname, session, baseScenario)
        try:
            cur = conn.cursor()
            cur.execute(sql_st)
            type = cur.fetchone()[0]
            conn.commit()
            cur.close()
            conn.close()
            if type is None: # in case it is an empty table
                return 0, False
            if type == 'rast':
                return 1, True
            return 1, type == scenType
        except psycopg2.Error, e:
            return 0, e.args[0]
    else:
        return 0, conn

def main():
    """
    For test purposes only.
    """
    #cur_ret, cur_obj = getPgCursor()
    #if cur_ret == 1:
    #    print cur_obj
    #cur_obj.close()
    #rows = testInsectionQuery()
    #rows = dwGetIntersectionArea(287)

    #rows = dwGetIntersectionArea(fieldId=287,areaType='')
    #for row in rows:
    #    print row

	#ret, rows = dwGetContacts()
	#print ret, rows

	#ret, rows = dwGetApplicators()
	#print ret, rows

    pass

if __name__ == '__main__':
    main()

