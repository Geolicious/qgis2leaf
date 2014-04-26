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


def qgis2leaf_exec(outputProjectFileName, basemapName, width, height, extent):
	# supply path to where is your qgis installed
	#QgsApplication.setPrefixPath("/path/to/qgis/installation", True)

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
	<div id="map" style="align: center;width:""" + width + """px; height: """ + height + """px"></div> <!-- this is the initial look of the map. in most cases it is done externally using something like a map.css stylesheet were you can specify the look of map elements, like background color tables and so on.-->
	<script src="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.js"></script> <!-- this is the javascript file that does the magic-->
  """
		f.write(base)
		f.close()
	# let's create the js files in the data folder of input vector files:
	canvas = qgis.utils.iface.mapCanvas()
	allLayers = canvas.layers()
	exp_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
	for i in allLayers: 
		if i.type() != 0 :
			print(i.name() + " skipped as it is not a vector layer")  
		if i.type() == 0 :
			
			qgis.core.QgsVectorFileWriter.writeAsVectorFormat(i,dataStore + os.sep + str(i.name()) + '.js', 'utf-8', exp_crs, 'GeoJson')
			#now change the data structure to work with leaflet:
			with open(dataStore + os.sep + str(i.name()) + '.js', "r+") as f2:
				old = f2.read() # read everything in the file
				f2.seek(0) # rewind
				f2.write("var " + str(i.name()) + " = " + old) # write the new line before
				f2.close
				
			#now add the js files as data input for our map
			with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f3:
				new_src = """
	<script src='""" + 'data' + os.sep + str(i.name()) + """.js' ></script>
	"""
				# store everything in the file
				f3.write(new_src)
				f3.close()
	#now determine the canvas bounding box
	#####now with viewcontrol
	if extent == 'canvas extent':
		pt0	= canvas.extent()
		crsSrc = qgis.utils.iface.mapCanvas().mapRenderer().destinationCrs()    # WGS 84
		crsDest = QgsCoordinateReferenceSystem(4326)  # WGS 84 / UTM zone 33N
		xform = QgsCoordinateTransform(crsSrc, crsDest)
		pt1 = xform.transform(pt0)
		bbox_canvas = [pt1.yMinimum(), pt1.yMaximum(),pt1.xMinimum(), pt1.xMaximum()]
		bounds = '[[' + str(pt1.yMinimum()) + ',' + str(pt1.xMinimum()) + '],[' + str(pt1.yMaximum()) + ',' + str(pt1.xMaximum()) +']]'
		middle = """
	<script>
		var map = L.map('map', { zoomControl:true }).fitBounds(""" + bounds + """);"""
	if extent == 'layer extent':
		middle = """
	<script>
		var map = L.map('map', { zoomControl:true });"""
	#here come the basemap our geojsons will  looped after that
	middle += """var feature_group = new L.featureGroup([]);
	"""
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
		if i.type() != 0 :
			print(i.name() + " skipped as it is not a vector layer")  
		if i.type() == 0 :
			with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f5:
				fields = i.pendingFields() 
				field_names = [field.name() for field in fields]
				tablestart = """'<table><tr><th>attribute</th><th>value</th></tr>"""
				row = ""
				for field in field_names:
					row += """<tr><td>""" + str(field) + """</td><td>' + feature.properties.""" + str(field) + """ + '</td></tr>"""
				tableend = """</table>'"""
				table = tablestart + row +tableend
				print table
				new_pop = """
		function pop_""" + i.name() + """(feature, layer) {
			var popupContent = """ + table + """;
			layer.bindPopup(popupContent);
		}
				"""
				
				new_obj = """
		var """ + i.name() + """JSON = new L.geoJson(""" + i.name() + """,{
			onEachFeature: pop_""" + i.name() + """,
			pointToLayer: function (feature, latlng) {
				return L.marker(latlng);
				}
			});
		feature_group.addLayer(""" + i.name() + """JSON);"""
		
				print new_obj
				# store everything in the file
				f5.write(new_pop)
				f5.write(new_obj)
				f5.write(i.name() + """JSON.addTo(map);""")
				f5.close()
	# let's add layer control
	controlStart = """
	L.control.layers({},{"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f6:
		f6.write(controlStart)
		f6.close()

	for i in allLayers: 
		if i.type() != 0 :
			print(i.name() + " skipped as it is not a vector layer")  
		if i.type() == 0 :
			with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f7:
				new_layer = '"' + i.name() + '"' + ": " + i.name() + """JSON,"""
				f7.write(new_layer)
				f7.close()

	controlEnd = "}).addTo(map);"	
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'rb+') as f8:
		f8.seek(-1, os.SEEK_END)
		f8.truncate()
		f8.write(controlEnd)
		f8.close()
	
	# let's close the file but ask for the extent of all layers if the user wants to show only this extent:
	if extent == 'layer extent':
		end = """
		map.fitBounds(feature_group.getBounds());
	</script>
</body>
</html>
	"""
	if extent == 'canvas extent':
		end = """
	</script>
</body>
</html>
	"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f9:
		f9.write(end)
		f9.close()
