#!/bin/csh -f
setenv MAPSERVER_HOME /web/groups/mapserve/util/mapserver
setenv LD_LIBRARY_PATH $MAPSERVER_HOME/lib:/usr/local/lib:/usr/lib
setenv CLASSPATH /web/groups/mapserve/public_html/rosa:/web/groups/mapserve/public_html/rosa/class
/web/groups/mapserve/public_html/cgi-bin/mapserv *
