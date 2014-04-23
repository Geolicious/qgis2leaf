# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgis2leaf
                                 A QGIS plugin
 QGIS to Leaflet creation programm
                             -------------------
        begin                : 2013-04-29
        copyright            : (C) 2013 by Riccardo Klinger
        email                : riccardo.klinger@geolicious.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 3 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4.QtCore import QFileInfo
import osgeo.ogr, osgeo.osr #we will need some packages
from osgeo import ogr
from qgis.core import *
import qgis.utils
import os #for file writing/folder actions
import shutil #for reverse removing directories
import urllib # to get files from the web


def qgis2leaf_exec(outputProjectFileName, basemapName):
	# supply path to where is your qgis installed
	QgsApplication.setPrefixPath("/path/to/qgis/installation", True)

	# load providers
	QgsApplication.initQgis()
	# let's determine the current work folder of qgis:
	print os.getcwd()

	# let's create the overall folder structure:
	if os.path.isdir(os.path.join(os.getcwd(),outputProjectFileName)):
		shutil.rmtree(str(os.path.join(os.getcwd(),outputProjectFileName)))
	jsStore = os.path.join(os.getcwd(),outputProjectFileName, 'js')
	os.makedirs(jsStore)
	dataStore = os.path.join(os.getcwd(),outputProjectFileName, 'data')
	os.makedirs(dataStore)
	cssStore = os.path.join(os.getcwd(),outputProjectFileName, 'css')
	os.makedirs(cssStore)
	picturesStore = os.path.join(os.getcwd(),outputProjectFileName, 'pictures')
	os.makedirs(picturesStore)
	miscStore = os.path.join(os.getcwd(),outputProjectFileName, 'misc')
	os.makedirs(miscStore)
	#the index file has an easy beginning. we will store it right away:
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'w') as f:
		base = """
<!DOCTYPE html>
<html>
<head>
	<title>QGIS2leaf webmap</title>
	<meta charset="utf-8" />
	<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.css" /> <!-- we will us e this as the styling script for our webmap-->
</head>
<body>
	<div id="map" style="align: center;width: 500px; height: 500px"></div> <!-- this is the initial look of the map. in most cases it is done externally using something like a map.css stylesheet were you can specify the look of map elements, like background color tables and so on.-->
	<script src="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.js"></script> <!-- this is the javascript file that does the magic-->
  """
		f.write(base)
		f.close()
	# let's create the js files in the data folder of input vector files:
	canvas = qgis.utils.iface.mapCanvas()
	allLayers = canvas.layers()
	for i in allLayers: 
		if i.type() != 0 :
			print(i.name() + " skipped as it is not a vector layer")  
		if i.type() == 0 :
			
			qgis.core.QgsVectorFileWriter.writeAsVectorFormat(i,dataStore + os.sep + str(i.name()) + '.js', 'utf-8', i.crs(), 'GeoJson')
			#now change the data structure to work with leaflet:
			with open(dataStore + os.sep + str(i.name()) + '.js', "r+") as f2:
				old = f2.read() # read everything in the file
				f2.seek(0) # rewind
				f2.write("var " + str(i.name()) + " = " + old) # write the new line before
				f2.close
				
			#now add the js files as data input for our map
			with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f3:
				new_src = """<script src='""" + dataStore + os.sep + str(i.name()) + """.js' ></script>"""
				# store everything in the file
				f3.write(new_src)
				f3.close()
	#here come the basemap our geojsons will  looped after that
	middle = """
	<script>
		var map = L.map('map', { zoomControl:true }).setView([0,0], 2);
		map.attributionControl.addAttribution("designed by <a href='http://www.geolicious.de' target='_blank'>Geolicious</a>; <a href='http://creativecommons.org/publicdomain/mark/1.0/' target='_blank'>markers license:</a>, basemap (Data CC-By-SA) by <a href='http://openstreetmap.org/' target='_blank'>OpenStreetMap</a>"); //ein paar Referenzen sollten in die Karte"
	"""
	print basemapName
	if basemapName == 'OSM Standard':
		basemapText = """
		L.tileLayer('http://a.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OSM Black & White':
		basemapText = """
		L.tileLayer('http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'Stamen Toner':
		basemapText = """
		L.tileLayer('http://a.tile.stamen.com/toner/{z}/{x}/{y}.png').addTo(map);
		"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f4:
			f4.write(middle)
			f4.write(basemapText)
			f4.close()
	for i in allLayers: 
		with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f5:
			new_obj = """var """ + i.name() + """JSON = new L.geoJson(""" + i.name() + """).addTo(map);"""
			# store everything in the file
			f5.write(new_obj)
			f5.close()
	# let's close the file
	end = """</script>
	</body>
	</html>
	"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f6:
		f6.write(end)
		f6.close()
