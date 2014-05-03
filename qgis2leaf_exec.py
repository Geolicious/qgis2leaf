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
import time
import re

def qgis2leaf_exec(outputProjectFileName, basemapName, width, height, extent, full, layer_list, visible):
	# supply path to where is your qgis installed
	#QgsApplication.setPrefixPath("/path/to/qgis/installation", True)

	# load providers
	QgsApplication.initQgis()
	# let's determine the current work folder of qgis:
	print os.getcwd()		
	print layer_list
	# let's create the overall folder structure:
	outputProjectFileName = os.path.join(outputProjectFileName, 'export_' + str(time.strftime("%Y_%m_%d")) + '_' + str(time.strftime("%I_%M_%S")))
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
	#lets create a css file for own css:
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'css' + os.sep + 'own_style.css', 'w') as f_css:
		if full == 1:
			text = """
<style>
	body {
		padding: 0;
		margin: 0;
	}
	html, body, #map {
		height: 100%;
		width: 100%;
	}
</style>"""
		if full == 0:
			text = """
<style>
	body {
		padding: 0;
		margin: 0;
	}
	html, body, #map {
		height: """+str(height)+"""px;
		width: """+str(width)+"""px;
	}
</style>"""
		f_css.write(text)
		f_css.close()
	
	#the index file has an easy beginning. we will store it right away:
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'w') as f_html:
		base = """
<!DOCTYPE html>
<html>
<head>
	<title>QGIS2leaf webmap</title>
	<meta charset="utf-8" />
	<link rel="stylesheet" href="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.css" /> <!-- we will us e this as the styling script for our webmap-->
	<link rel="stylesheet" type="text/css" href="css/own_style.css">
</head>
<body>
	<div id="map"></div> <!-- this is the initial look of the map. in most cases it is done externally using something like a map.css stylesheet were you can specify the look of map elements, like background color tables and so on.-->
	<script src="http://cdn.leafletjs.com/leaflet-0.7.2/leaflet.js"></script> <!-- this is the javascript file that does the magic-->
  """
		f_html.write(base)
		f_html.close()
	# let's create the js files in the data folder of input vector files:
	canvas = qgis.utils.iface.mapCanvas()
	allLayers = canvas.layers()
	exp_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
	for i in allLayers: 
		for j in layer_list:
			if re.sub('[\W_]+', '', i.name()) == re.sub('[\W_]+', '', j):
				qgis.core.QgsVectorFileWriter.writeAsVectorFormat(i,dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js', 'utf-8', exp_crs, 'GeoJson')
				#now change the data structure to work with leaflet:
				with open(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js', "r+") as f2:
					old = f2.read() # read everything in the file
					f2.seek(0) # rewind
					print str(re.sub('[\W_]+', '', i.name()))
					f2.write("var exp_" + str(re.sub('[\W_]+', '', i.name())) + " = " + old) # write the new line before
					f2.close
					
				#now add the js files as data input for our map
				with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f3:
					new_src = """
		<script src='""" + 'data' + os.sep + """exp_""" + re.sub('[\W_]+', '', i.name()) + """.js' ></script>
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
	#here come the basemap (variants list thankfully provided by: "https://github.com/leaflet-extras/leaflet-providers") our geojsons will  looped after that
	middle += """
	var feature_group = new L.featureGroup([]);
	"""
	if basemapName == 'OSM Standard':
		basemapText = """
		map.attributionControl.addAttribution('&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OSM Black & White':
		basemapText = """
		map.attributionControl.addAttribution('&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'Stamen Toner':
		basemapText = """
		map.attributionControl.addAttribution('Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>');
		L.tileLayer('http://a.tile.stamen.com/toner/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OSM DE':
		basemapText = """
		map.attributionControl.addAttribution('&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OSM HOT':
		basemapText = """
		map.attributionControl.addAttribution('&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>'); 
		L.tileLayer('http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png').addTo(map);
		"""	
	if basemapName == 'OpenSeaMap':
		basemapText = """
		map.attributionControl.addAttribution('Map data: &copy; <a href="http://www.openseamap.org">OpenSeaMap</a> contributors'); 
		L.tileLayer('http://tiles.openseamap.org/seamark/{z}/{x}/{y}.png').addTo(map);
		"""		
	if basemapName == 'Thunderforest Cycle':
		basemapText = """
		map.attributionControl.addAttribution('&copy; <a href="http://www.opencyclemap.org">OpenCycleMap</a>, &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png').addTo(map);
		"""	
	if basemapName == 'Thunderforest Transport':
		basemapText = """
		map.attributionControl.addAttribution('&copy; <a href="http://www.opencyclemap.org">OpenCycleMap</a>, &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.thunderforest.com/transport/{z}/{x}/{y}.png').addTo(map);
		"""			
	if basemapName == 'Thunderforest Landscape':
		basemapText = """
		map.attributionControl.addAttribution('&copy; <a href="http://www.opencyclemap.org">OpenCycleMap</a>, &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png').addTo(map);
		"""	
	if basemapName == 'Thunderforest Outdoors':
		basemapText = """
		map.attributionControl.addAttribution('&copy; <a href="http://www.opencyclemap.org">OpenCycleMap</a>, &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png').addTo(map);
		"""		
	if basemapName == 'OpenMapSurfer Roads':
		basemapText = """
		map.attributionControl.addAttribution('Imagery from <a href="http://giscience.uni-hd.de/">GIScience Research Group @ University of Heidelberg</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://openmapsurfer.uni-hd.de/tiles/roads/x={x}&y={y}&z={z}').addTo(map);
		"""			
	if basemapName == 'OpenMapSurfer adminb':
		basemapText = """
		map.attributionControl.addAttribution('Imagery from <a href="http://giscience.uni-hd.de/">GIScience Research Group @ University of Heidelberg</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://openmapsurfer.uni-hd.de/tiles/adminb/x={x}&y={y}&z={z}').addTo(map);
		"""	
	if basemapName == 'OpenMapSurfer roadsg':
		basemapText = """
		map.attributionControl.addAttribution('Imagery from <a href="http://giscience.uni-hd.de/">GIScience Research Group @ University of Heidelberg</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://openmapsurfer.uni-hd.de/tiles/roadsg/x={x}&y={y}&z={z}').addTo(map);
		"""
	if basemapName == 'MapQuestOpen OSM':
		basemapText = """
		map.attributionControl.addAttribution('Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://otile1.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg').addTo(map);
		"""	
	if basemapName == 'MapQuestOpen Aerial':
		basemapText = """
		map.attributionControl.addAttribution('Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency'); 
		L.tileLayer('http://otile1.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg').addTo(map);
		"""
	if basemapName == 'Stamen Terrain':
		basemapText = """
		map.attributionControl.addAttribution('Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>');
		L.tileLayer('http://a.tile.stamen.com/terrain/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'Stamen Watercolor':
		basemapText = """
		map.attributionControl.addAttribution('Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>');
		L.tileLayer('http://a.tile.stamen.com/watercolor/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Clouds':
		basemapText = """
		map.attributionControl.addAttribution('Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/clouds/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Precipitation':
		basemapText = """
		map.attributionControl.addAttribution('Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/precipitation/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Rain':
		basemapText = """
		map.attributionControl.addAttribution('Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/rain/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Pressure':
		basemapText = """
		map.attributionControl.addAttribution('Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/pressure/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Wind':
		basemapText = """
		map.attributionControl.addAttribution('Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/wind/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Temp':
		basemapText = """
		map.attributionControl.addAttribution('Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/temp/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Snow':
		basemapText = """
		map.attributionControl.addAttribution('Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/snow/{z}/{x}/{y}.png').addTo(map);
		"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f4:
			f4.write(middle)
			f4.write(basemapText)
			f4.close()
	for i in allLayers: 
		for j in layer_list:
			if re.sub('[\W_]+', '', i.name()) == j:
				with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f5:
					fields = i.pendingFields() 
					field_names = [field.name() for field in fields]
					html_prov = False
					for field in field_names:
						if str(field) == 'html_exp':
							html_prov = True
							table = 'feature.properties.html_exp'
							break
					if html_prov != True:
						tablestart = """'<table><tr><th>attribute</th><th>value</th></tr>"""
						row = ""
						for field in field_names:
							row += """<tr><td>""" + str(field) + """</td><td>' + feature.properties.""" + str(field) + """ + '</td></tr>"""
						tableend = """</table>'"""
						table = tablestart + row +tableend
					print table
					new_pop = """
			function pop_""" + re.sub('[\W_]+', '', i.name()) + """(feature, layer) {
				var popupContent = """ + table + """;
				layer.bindPopup(popupContent);
			}
					"""
					
					new_obj = """
			var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
				onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
				pointToLayer: function (feature, latlng) {
					return L.marker(latlng);
					}
				});
			feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
			"""
			
					print new_obj
					# store everything in the file
					f5.write(new_pop)
					f5.write(new_obj)
					if visible == 'show all':
						f5.write("""
					//add comment sign to hide this layer on the map in the initial view.
					exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON.addTo(map);""")
					if visible == 'show none':
						f5.write("""
					//delete comment sign to show this layer on the map in the initial view.
					//exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON.addTo(map);""")
					f5.close()
	# let's add layer control
	controlStart = """
	L.control.layers({},{"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f6:
		f6.write(controlStart)
		f6.close()

	for i in allLayers: 
		for j in layer_list:
			if re.sub('[\W_]+', '', i.name()) == re.sub('[\W_]+', '', j):
				with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f7:
					new_layer = '"' + re.sub('[\W_]+', '', i.name()) + '"' + ": exp_" + re.sub('[\W_]+', '', i.name()) + """JSON,"""
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
