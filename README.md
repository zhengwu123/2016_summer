# 2016_summer intern GIS

# sprint 1 learn openlayer API and do some exaple practices
Process - copy some of the [http://openlayers.org/en/latest/examples/tutorials] to your

buckeye drive, get them to work. Then improve them with our local data.
simple map with "vector" layer:
----

http://openlayers.org/en/latest/examples/simple.html

---- 
http://openlayers.org/en/latest/examples/geojson.html

geoserver can provide geojason on requst, and the request may be filtered.


http://openlayers.org/en/latest/examples/vector-layer.html

can you make this geojson tutorial work with our data? 
Use geoserver layer preview to get familiar with the data.
[ http://buckeye.agriculture.purdue.edu/geoserver/web/?

wicket:bookmarkablePage=:org.geoserver.web.demo.MapPreviewPage]

To look at the structure of the map layer "states" you can request it in GML from layer

preview, which will show how it is organized.
[http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?

service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50 ]

To  query "states" as json (to replace object in demo do this:

[ http://buckeye.agriculture.purdue.edu/geoserver/topp/ows?

service=WFS&version=1.0.0&request=GetFeature&typeName=topp:states&maxFeatures=50&outputFor

mat=application%2Fjson ]


M O R E    E X A M P L E S


map a less simple map:

http://openlayers.org/en/latest/examples/wms-tiled.html
read what is WMS here http://docs.geoserver.org/stable/en/user/services/wms/index.html

---------
maps that allow drawing:

http://openlayers.org/en/latest/examples/draw-features.html
select shape and then draw

http://openlayers.org/en/latest/examples/draw-and-modify-features.html
draw and edit shapes

http://openlayers.org/en/latest/examples/modify-test.html

-----------  more advanced maps:

http://openlayers.org/en/latest/examples/vector-wfs.html
WFS is important data source; read WFS format definition here

http://docs.geoserver.org/stable/en/user/services/wfs/index.html

---------


http://openlayers.org/en/latest/examples/raster.html
we will deal with lots of raster data.

http://openlayers.org/en/latest/examples/mouse-position.html
to capture location as position


fetching data 
http://openlayers.org/en/latest/examples/getfeatureinfo-layers.html

fetching ESRI data

http://openlayers.org/en/latest/examples/vector-esri.html
we currently do not use ESRI formated data, but we might add it.
# sprint 1 end

#Sprint 2 start

For the second sprint in the summer session, we will learn Python and bring together things you worked on in the first sprint. You will use HTML, JavaScript, mapping API’s and Python.
So from today, May 31 until June 8, you should learn Python using the resources I sent out or discover better for yourself. I suggest a holistic approach but I have a specific task set. 
Here is the task. You need to create an HTML page in the mapserve directory with four buttons. When the page opens we see a map of topp:states from buckeye.agriculture.purdue.edu/geoserver  . This layer is displayer over Open Street Map background ( so you do not need to mess with a Google key for aerial photos unless you want to.)
(Link to the states layer just to help you,  [http://buckeye.agriculture.purdue.edu/geoserver/topp/wms?service=WMS&version=1.1.0&request=GetMap&layers=topp:states&styles=&bbox=-124.73142200000001,24.955967,-66.969849,49.371735&width=768&height=330&srs=EPSG:4326&format=application/openlayers] )
When the page is opened, the users sees “states” drawn (preferably semi-transparent) over Open Street Map (OSM). But there should be a checkbox to turn off the display of the states layer. 
Hint – use variable names for the layer because all 4 of your layers will use checkboxes to turn on and off and it will be much faster to have an outside JS file that assigns variable names and then in your HTML page, use the variable names with the checkboxes to turn on and off. 
Button one on your page runs a python script to do a CQL query to fetch the state where STATE_NAME = “Indiana”. It should display on map and have a checkbox to turn on and off. This layer should have a pop-up enabled.
Button two on your page runs a python script to do a CQL query to fetch the state where STATE_NAME = “Michigan”. It should display on map and have a checkbox to turn on and off. This layer should have a pop-up enabled.
Button three on your page runs a python script to do a CQL query to fetch the state where STATE_NAME = “Ohio”. It should display on map and have a checkbox to turn on and off. This layer should have a pop-up enabled.
Button Four reports the state of the button 1-3 checkboxes to a Python script. In other words, the user is making a selection of a subset of the three states using the checkboxes and you need to pass to a script the choices the user made, using a list of the selected states but not the unselected states, at any time when the user hits button 4 to run the “select and export list” script. When the user hits button 4, your Python script is fired. 
You need to write a Python script that will fire from the button and print or display the selected state names. That is a mock-up of selecting input from the map page and sending It to the Python model scripts. So you will need to learn how to make Apache read as cgi and execute Python on the server in the mapserve account. You need to make .py change to .cgi and use this line at the top:
# sprint 2 finished

