# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgis2leaf
                                 A QGIS plugin
 QGIS to Leaflet creation programm
                             -------------------
        begin                : 2014-04-29
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
from osgeo import gdal
import subprocess
import shutil
from qgis.core import *
import qgis.utils
import os #for file writing/folder actions
import shutil #for reverse removing directories
import urllib # to get files from the web
import time
import re
import fileinput
import webbrowser #to open the made map directly in your browser
import sys #to use another print command without annoying newline characters 


def layerstyle_single(layer):
	return color_code

def qgis2leaf_exec(outputProjectFileName, basemapName, width, height, extent, full, layer_list, visible, opacity_raster):
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
"""
		elif full == 0:
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
"""
		if opacity_raster == True and full == 1:
			text += """
				html, body, #slide {
		margin-left: auto;
		margin-right: auto;
		width: 100%;
</style>"""
		elif opacity_raster == True and full== 0:
			text += """	
		html, body, #slide {
		margin-left: auto;
		margin-right: auto;
		width: """+str(width)+"""px;
</style>"""
		elif opacity_raster == False:
			text += """
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
	
	<link rel="stylesheet" href="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.2/leaflet.css" /> <!-- we will us e this as the styling script for our webmap-->
	<link rel="stylesheet" type="text/css" href="css/own_style.css">
</head>
<body>
	<div id="map"></div> <!-- this is the initial look of the map. in most cases it is done externally using something like a map.css stylesheet were you can specify the look of map elements, like background color tables and so on.-->
	<script src="http://cdnjs.cloudflare.com/ajax/libs/leaflet/0.7.2/leaflet.js"></script> <!-- this is the javascript file that does the magic-->
	"""
		if opacity_raster == True:
			base += """<input id="slide" type="range" min="0" max="1" step="0.1" value="1" onchange="updateOpacity(this.value)">"""
  		f_html.write(base)
		f_html.close()
	# let's create the js files in the data folder of input vector files:
	canvas = qgis.utils.iface.mapCanvas()
	allLayers = canvas.layers()
	exp_crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.EpsgCrsId)
	for i in allLayers: 
		for j in layer_list:
			if re.sub('[\W_]+', '', i.name()) == re.sub('[\W_]+', '', j):
				if i.type() ==0:
					qgis.core.QgsVectorFileWriter.writeAsVectorFormat(i,dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js', 'utf-8', exp_crs, 'GeoJson')
					#now change the data structure to work with leaflet:

					with open(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js', "r+") as f2:
						old = f2.read() # read everything in the file
						f2.seek(0) # rewind
						#print str(re.sub('[\W_]+', '', i.name()))
						f2.write("var exp_" + str(re.sub('[\W_]+', '', i.name())) + " = " + old) # write the new line before
						f2.close
					#let's define style for the single marker points
					if i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 0:
						color_str = str(i.rendererV2().symbol().color().name())
						radius_str = str(i.rendererV2().symbol().size() * 2)
						transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
						transp_str2 = str(i.rendererV2().symbol().alpha())
						for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
							line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "color_qgis2leaf": '""" + color_str + """', "radius_qgis2leaf": """ + radius_str + """, "transp_qgis2leaf": """ + transp_str + """, "transp_fill_qgis2leaf": """ + transp_str2 + """, """ )
							sys.stdout.write(line)
					#let's define style for the single marker lines
					if i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 1:
						color_str = str(i.rendererV2().symbol().color().name())
						radius_str = str(i.rendererV2().symbol().width() * 5)
						transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
						transp_str2 = str(i.rendererV2().symbol().alpha())
						for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
							line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "color_qgis2leaf": '""" + color_str + """', "radius_qgis2leaf": """ + radius_str + """, "transp_qgis2leaf": """ + transp_str + """, "transp_fill_qgis2leaf": """ + transp_str2 + """, """ )
							sys.stdout.write(line)
					#let's define style for the single marker polygons
					if i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 2:
						color_str = str(i.rendererV2().symbol().color().name())
						borderColor_str = str(i.rendererV2().symbol().symbolLayer(0).borderColor().name())
						radius_str = str(i.rendererV2().symbol().symbolLayer(0).borderWidth() * 5)
						transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
						transp_str2 = str(i.rendererV2().symbol().alpha())
						for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
							line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "color_qgis2leaf": '""" + color_str + """', "border_color_qgis2leaf": '""" + borderColor_str + """', "radius_qgis2leaf": """ + radius_str + """, "transp_qgis2leaf": """ + transp_str + """, "transp_fill_qgis2leaf": """ + transp_str2 + """, """ )
							sys.stdout.write(line)		
					#let's define style for categorized points
					if i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 0:
						iter = i.getFeatures()
						provider = i.dataProvider()
						attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())
						categories = i.rendererV2().categories()
						color_str = []
						radius_str = []
						transp_str2 = []
						transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
						for feat in iter:
							fid = feat.id()
							attribute_map = feat.attributes()
							catindex = i.rendererV2().categoryIndexForValue(str(attribute_map[attrvalindex]))
	    					#print catindex
							if catindex != -1: 
								color_str.append(str(categories[catindex].symbol().color().name()))
								radius_str.append(str(categories[catindex].symbol().size() * 2))
								transp_str2.append(str(categories[catindex].symbol().alpha()))
							else: 
								color_str.append('#FF00FF')
								radius_str.append('4')
								transp_str2.append('1')
							#print color_str
						qgisLeafId = 0
						for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
							addOne = str(line).count(""""type": "Feature", "properties": { """)
							if qgisLeafId < len(color_str):
								line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "radius_qgis2leaf": """ + str(radius_str[qgisLeafId]) + """, "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
							else:
								line = line.replace(" "," ")
							sys.stdout.write(line)
							qgisLeafId = qgisLeafId+addOne
						
					#let's define style for categorized lines
					if i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 1:
						iter = i.getFeatures()
						provider = i.dataProvider()
						attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())
						categories = i.rendererV2().categories()
						color_str = []
						radius_str = []
						transp_str2 = []
						transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
						for feat in iter:
							fid = feat.id()
							attribute_map = feat.attributes()
							catindex = i.rendererV2().categoryIndexForValue(str(attribute_map[attrvalindex]))
	    					#print catindex
							if catindex != -1: 
								color_str.append(str(categories[catindex].symbol().color().name()))
								radius_str.append(str(categories[catindex].symbol().width() * 5))
								transp_str2.append(str(categories[catindex].symbol().alpha()))
							else: 
								color_str.append('#FF00FF')
								radius_str.append('4')
								transp_str2.append('1')
							#print color_str
						qgisLeafId = 0
						for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
							addOne = str(line).count(""""type": "Feature", "properties": { """)
							if qgisLeafId < len(color_str):
								line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "radius_qgis2leaf": """ + str(radius_str[qgisLeafId]) + """, "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
							else:
								line = line.replace(" "," ")
							sys.stdout.write(line)
							qgisLeafId = qgisLeafId+addOne
					#let's define style for categorized polygons
					if i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 2:
						iter = i.getFeatures()
						provider = i.dataProvider()
						attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())
						categories = i.rendererV2().categories()
						color_str = []
						radius_str = []
						transp_str2 = []
						transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
						for feat in iter:
							fid = feat.id()
							attribute_map = feat.attributes()
							catindex = i.rendererV2().categoryIndexForValue(str(attribute_map[attrvalindex]))
	    					#print catindex
							if catindex != -1: 
								color_str.append(str(categories[catindex].symbol().color().name()))
								transp_str2.append(str(categories[catindex].symbol().alpha()))
							else: 
								color_str.append('#FF00FF')
								transp_str2.append('1')
							#print color_str
						qgisLeafId = 0
						for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
							addOne = str(line).count(""""type": "Feature", "properties": { """)
							if qgisLeafId < len(color_str):
								line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
							else:
								line = line.replace(" "," ")
							sys.stdout.write(line)
							qgisLeafId = qgisLeafId+addOne	
					#let's define style for the graduaded marker points
					if i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 0:
						# every json entry needs a unique id:
						iter = i.getFeatures()
						#what is the value based on:
						provider = i.dataProvider()
						attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())	
						transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
						color_str = []
						radius_str = []
						transp_str2 = []
						for feat in iter:
							if str(feat.attributes()[attrvalindex]) != 'NULL':
								value = int(feat.attributes()[attrvalindex])
							elif str(feat.attributes()[attrvalindex]) == 'NULL':
								value = None
							for r in i.rendererV2().ranges():
								if value >= r.lowerValue() and value <= r.upperValue() and value != None:
									#print r.lowerValue()
									#print r.upperValue()
									color_str.append(str(r.symbol().color().name()))
									radius_str.append(str(r.symbol().size() * 2))
									transp_str2.append(str(r.symbol().alpha()))
									break
									#print r.symbol().color().name()
								elif value == None:
									color_str.append('#FF00FF')
									radius_str.append('4')
									transp_str2.append('1')
									break
						qgisLeafId = 0
						for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
							addOne = str(line).count(""""type": "Feature", "properties": { """)
							if qgisLeafId < len(color_str):
								line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "radius_qgis2leaf": """ + str(radius_str[qgisLeafId]) + """, "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
							else:
								line = line.replace(" "," ")
							sys.stdout.write(line)
							qgisLeafId = qgisLeafId+addOne
							
					#let's define style for the graduaded marker line
					if i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 1:
						# every json entry needs a unique id:
						iter = i.getFeatures()
						#what is the value based on:
						provider = i.dataProvider()
						attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())	
						transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
						color_str = []
						radius_str = []
						transp_str2 = []
						for feat in iter:
							if str(feat.attributes()[attrvalindex]) != 'NULL':
								value = int(feat.attributes()[attrvalindex])
							elif str(feat.attributes()[attrvalindex]) == 'NULL':
								value = None
							for r in i.rendererV2().ranges():
								if value >= r.lowerValue() and value <= r.upperValue() and value != None:
									print r.lowerValue()
									print r.upperValue()
									color_str.append(str(r.symbol().color().name()))
									radius_str.append(str(r.symbol().width() * 5))
									transp_str2.append(str(r.symbol().alpha()))
									break
									print r.symbol().color().name()
								elif value == None:
									color_str.append('#FF00FF')
									radius_str.append('4')
									transp_str2.append('1')
									break
						qgisLeafId = 0
						for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
							addOne = str(line).count(""""type": "Feature", "properties": { """)
							if qgisLeafId < len(color_str):
								line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "radius_qgis2leaf": """ + str(radius_str[qgisLeafId]) + """, "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
							else:
								line = line.replace(" "," ")
							sys.stdout.write(line)
							qgisLeafId = qgisLeafId+addOne
					#let's define style for the graduaded marker polygon
					if i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 2:
						# every json entry needs a unique id:
						iter = i.getFeatures()
						#what is the value based on:
						provider = i.dataProvider()
						attrvalindex = provider.fieldNameIndex(i.rendererV2().classAttribute())	
						transp_str = str(1 - ( float(i.layerTransparency()) / 100 ) )
						color_str = []
						radius_str = []
						transp_str2 = []
						for feat in iter:
							if str(feat.attributes()[attrvalindex]) != 'NULL':
								value = int(feat.attributes()[attrvalindex])
							elif str(feat.attributes()[attrvalindex]) == 'NULL':
								value = None
							for r in i.rendererV2().ranges():
								if value >= r.lowerValue() and value <= r.upperValue() and value != None:
									print r.lowerValue()
									print r.upperValue()
									color_str.append(str(r.symbol().color().name()))
									transp_str2.append(str(r.symbol().alpha()))
									break
									print r.symbol().color().name()
								elif value == None:
									color_str.append('#FF00FF')
									transp_str2.append('1')
									break
						qgisLeafId = 0
						for line in fileinput.FileInput(dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.js',inplace=1):
							addOne = str(line).count(""""type": "Feature", "properties": { """)
							if qgisLeafId < len(color_str):
								line = line.replace(""""type": "Feature", "properties": { """,""""type": "Feature", "properties": { "id_qgis2leaf": """ + str(qgisLeafId) + """, "color_qgis2leaf": '""" + str(color_str[qgisLeafId]) + """', "transp_qgis2leaf": """ + str(transp_str) + """, "transp_fill_qgis2leaf": """ + str(transp_str2[qgisLeafId]) + """, """ )
							else:
								line = line.replace(" "," ")
							sys.stdout.write(line)
							qgisLeafId = qgisLeafId+addOne						
						
					#now add the js files as data input for our map
					with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f3:
						new_src = """
			<script src='""" + 'data' + os.sep + """exp_""" + re.sub('[\W_]+', '', i.name()) + """.js' ></script>
			"""
						# store everything in the file
						f3.write(new_src)
						f3.close()
				#here comes the raster layers. you need an installed version of gdal
				elif i.type() == 1:
					print i.name()
					filename_raster = str(i.dataProvider().dataSourceUri())
					ret = 0
					ret2 = 0
					out_raster_name = dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.jpg'

					if str(i.dataProvider().metadata()[0:4]) == 'JPEG' and str(i.crs().authid()) == 'EPSG:4326':
					#print out_raster_name
					#print('gdal_translate -of jpeg -outsize 100% 100% ' + filename_raster + " " +  out_raster_name)
						shutil.copyfile(filename_raster+".aux.xml", out_raster_name + ".aux.xml")
						shutil.copyfile(filename_raster, out_raster_name)
					else:
						ret = subprocess.check_call(['gdal_translate -of jpeg -outsize 100% 100% -a_srs EPSG:4326 ' + filename_raster + " " +  out_raster_name], shell=True)
						#ret2 = subprocess.check_call(['cp ' + filename_raster + ".aux.xml " +  out_raster_name + ".aux.xml"], shell=True)
					if ret != 0:
						print "translating your raster to jpg failed"
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
		var map = L.map('map', { zoomControl:true }).fitBounds(""" + bounds + """);
		var additional_attrib = 'created w. <a href="https://github.com/geolicious/qgis2leaf" target ="_blank">gis2leaf</a> by <a href="http://www.geolicious.de" target ="_blank">Geolicious</a> & contributors<br>';"""
	if extent == 'layer extent':
		middle = """
	<script>
		var map = L.map('map', { zoomControl:true });
		var additional_attrib = 'created with <a href="https://github.com/geolicious/qgis2leaf" target ="_blank">gis2leaf</a> by <a href="http://www.geolicious.de" target ="_blank">Geolicious</a> & contributors<br>';"""
	#here come the basemap (variants list thankfully provided by: "https://github.com/leaflet-extras/leaflet-providers") our geojsons will  looped after that
	middle += """
	var feature_group = new L.featureGroup([]);
	var raster_group = new L.LayerGroup([]);
	"""
	
	if basemapName == 'OSM Standard':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OSM Black & White':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.www.toolserver.org/tiles/bw-mapnik/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'Stamen Toner':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>');
		L.tileLayer('http://a.tile.stamen.com/toner/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OSM DE':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OSM HOT':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + '&copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Tiles courtesy of <a href="http://hot.openstreetmap.org/" target="_blank">Humanitarian OpenStreetMap Team</a>'); 
		L.tileLayer('http://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png').addTo(map);
		"""	
	if basemapName == 'OpenSeaMap':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Map data: &copy; <a href="http://www.openseamap.org">OpenSeaMap</a> contributors'); 
		L.tileLayer('http://tiles.openseamap.org/seamark/{z}/{x}/{y}.png').addTo(map);
		"""		
	if basemapName == 'Thunderforest Cycle':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + '&copy; <a href="http://www.opencyclemap.org">OpenCycleMap</a>, &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.thunderforest.com/cycle/{z}/{x}/{y}.png').addTo(map);
		"""	
	if basemapName == 'Thunderforest Transport':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + '&copy; <a href="http://www.opencyclemap.org">OpenCycleMap</a>, &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.thunderforest.com/transport/{z}/{x}/{y}.png').addTo(map);
		"""			
	if basemapName == 'Thunderforest Landscape':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + '&copy; <a href="http://www.opencyclemap.org">OpenCycleMap</a>, &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.thunderforest.com/landscape/{z}/{x}/{y}.png').addTo(map);
		"""	
	if basemapName == 'Thunderforest Outdoors':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + '&copy; <a href="http://www.opencyclemap.org">OpenCycleMap</a>, &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://{s}.tile.thunderforest.com/outdoors/{z}/{x}/{y}.png').addTo(map);
		"""		
	if basemapName == 'OpenMapSurfer Roads':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Imagery from <a href="http://giscience.uni-hd.de/">GIScience Research Group @ University of Heidelberg</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://openmapsurfer.uni-hd.de/tiles/roads/x={x}&y={y}&z={z}').addTo(map);
		"""			
	if basemapName == 'OpenMapSurfer adminb':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Imagery from <a href="http://giscience.uni-hd.de/">GIScience Research Group @ University of Heidelberg</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://openmapsurfer.uni-hd.de/tiles/adminb/x={x}&y={y}&z={z}').addTo(map);
		"""	
	if basemapName == 'OpenMapSurfer roadsg':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Imagery from <a href="http://giscience.uni-hd.de/">GIScience Research Group @ University of Heidelberg</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://openmapsurfer.uni-hd.de/tiles/roadsg/x={x}&y={y}&z={z}').addTo(map);
		"""
	if basemapName == 'MapQuestOpen OSM':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>'); 
		L.tileLayer('http://otile1.mqcdn.com/tiles/1.0.0/map/{z}/{x}/{y}.jpeg').addTo(map);
		"""	
	if basemapName == 'MapQuestOpen Aerial':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Tiles Courtesy of <a href="http://www.mapquest.com/">MapQuest</a> &mdash; Portions Courtesy NASA/JPL-Caltech and U.S. Depart. of Agriculture, Farm Service Agency'); 
		L.tileLayer('http://otile1.mqcdn.com/tiles/1.0.0/sat/{z}/{x}/{y}.jpg').addTo(map);
		"""
	if basemapName == 'Stamen Terrain':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>');
		L.tileLayer('http://a.tile.stamen.com/terrain/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'Stamen Watercolor':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Map tiles by <a href="http://stamen.com">Stamen Design</a>, <a href="http://creativecommons.org/licenses/by/3.0">CC BY 3.0</a> &mdash; Map data: &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors,<a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>');
		L.tileLayer('http://a.tile.stamen.com/watercolor/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Clouds':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/clouds/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Precipitation':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/precipitation/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Rain':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/rain/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Pressure':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/pressure/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Wind':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/wind/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Temp':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/temp/{z}/{x}/{y}.png').addTo(map);
		"""
	if basemapName == 'OpenWeatherMap Snow':
		basemapText = """
		map.attributionControl.addAttribution(additional_attrib + 'Map data &copy; <a href="http://openweathermap.org">OpenWeatherMap</a>'); 
		L.tileLayer('http://{s}.tile.openweathermap.org/map/snow/{z}/{x}/{y}.png').addTo(map);
		"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f4:
			f4.write(middle)
			f4.write(basemapText)
			f4.close()
	for i in allLayers: 
		for j in layer_list:
			if re.sub('[\W_]+', '', i.name()) == j:
				if i.type()==0:
					with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f5:
						#here comes the layer style
						#here comes the html popup content
						fields = i.pendingFields() 
						field_names = [field.name() for field in fields]
						html_prov = False
						icon_prov = False
						for field in field_names:
							if str(field) == 'html_exp':
								html_prov = True
								table = 'feature.properties.html_exp'
							if str(field) == 'icon_exp':
								icon_prov = True #we need this later on for icon creation
						if html_prov != True:
							tablestart = """'<table><tr><th>attribute</th><th>value</th></tr>"""
							row = ""
							for field in field_names:
								if str(field) == "icon_exp":
									row += ""
								else: 
									row += """<tr><td>""" + str(field) + """</td><td>' + feature.properties.""" + str(field) + """ + '</td></tr>"""
							tableend = """</table>'"""
							table = tablestart + row +tableend
						#print table
						new_pop = """
				function pop_""" + re.sub('[\W_]+', '', i.name()) + """(feature, layer) {
					var popupContent = """ + table + """;
					layer.bindPopup(popupContent);
				}
						"""
						#single marker points:
						 
						if i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 0 and icon_prov != True:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					pointToLayer: function (feature, latlng) {  
						return L.circleMarker(latlng, {
							radius: feature.properties.radius_qgis2leaf,
							fillColor: feature.properties.color_qgis2leaf,
							color: '#000',
							weight: 1,
							opacity: feature.properties.transp_qgis2leaf,
							fillOpacity: feature.properties.transp_fill_qgis2leaf
							})
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
						elif i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 1:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {weight: feature.properties.radius_qgis2leaf,
								color: feature.properties.color_qgis2leaf,
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_fill_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
						elif i.rendererV2().dump()[0:6] == 'SINGLE' and i.geometryType() == 2:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {color: feature.properties.border_color_qgis2leaf,
								fillColor: feature.properties.color_qgis2leaf,
								weight: feature.properties.radius_qgis2leaf,
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_fill_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""	
						elif i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 0 and icon_prov != True:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					pointToLayer: function (feature, latlng) {  
						return L.circleMarker(latlng, {
							radius: feature.properties.radius_qgis2leaf,
							fillColor: feature.properties.color_qgis2leaf,
							color: '#000',
							weight: 1,
							opacity: feature.properties.transp_qgis2leaf,
							fillOpacity: feature.properties.transp_fill_qgis2leaf
							})
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
						elif i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 1:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {weight: feature.properties.radius_qgis2leaf,
								color: feature.properties.color_qgis2leaf,
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_fill_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
						elif i.rendererV2().dump()[0:11] == 'CATEGORIZED' and i.geometryType() == 2:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {color: feature.properties.color_qgis2leaf,
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_fill_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""				
						elif i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 0 and icon_prov != True:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					pointToLayer: function (feature, latlng) {  
						return L.circleMarker(latlng, {
							radius: feature.properties.radius_qgis2leaf,
							fillColor: feature.properties.color_qgis2leaf,
							color: '#000',
							weight: 1,
							opacity: feature.properties.transp_qgis2leaf,
							fillOpacity: feature.properties.transp_fill_qgis2leaf
							})
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
						elif i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 1:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {weight: feature.properties.radius_qgis2leaf,
								color: feature.properties.color_qgis2leaf,
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_fill_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""	
						elif i.rendererV2().dump()[0:9] == 'GRADUATED' and i.geometryType() == 2:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					style: function (feature) {
						return {color: feature.properties.color_qgis2leaf,
								opacity: feature.properties.transp_qgis2leaf,
								fillOpacity: feature.properties.transp_fill_qgis2leaf};
						}
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
						elif icon_prov == True and i.geometryType() == 0:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					pointToLayer: function (feature, latlng) {
						return L.marker(latlng, {icon: L.icon({
							iconUrl: feature.properties.icon_exp,
							iconSize:     [48, 48], // size of the icon change this to scale your icon (first coordinate is x, second y from the upper left corner of the icon)
							iconAnchor:   [24, 24], // point of the icon which will correspond to marker's location (first coordinate is x, second y from the upper left corner of the icon)
							popupAnchor:  [0, -26] // point from which the popup should open relative to the iconAnchor (first coordinate is x, second y from the upper left corner of the icon)
			 				})
			 			})
					}}
				);
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
						else:
							new_obj = """
				var exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON = new L.geoJson(exp_""" + re.sub('[\W_]+', '', i.name()) + """,{
					onEachFeature: pop_""" + re.sub('[\W_]+', '', i.name()) + """,
					});
				feature_group.addLayer(exp_""" + re.sub('[\W_]+', '', i.name()) + """JSON);
				"""		
				
						#print new_obj
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
				elif i.type() == 1:
					print "this is a raster"
					out_raster_name = dataStore + os.sep + 'exp_' + re.sub('[\W_]+', '', i.name()) + '.jpg'
					pt2	= i.extent()
					print pt2
					crsSrc = i.crs()    # WGS 84
					crsDest = QgsCoordinateReferenceSystem(4326)  # WGS 84 / UTM zone 33N
					xform = QgsCoordinateTransform(crsSrc, crsDest)
					pt3 = xform.transform(pt2)
					bbox_canvas2 = [pt3.yMinimum(), pt3.yMaximum(),pt3.xMinimum(), pt3.xMaximum()]
					bounds2 = '[[' + str(pt3.yMinimum()) + ',' + str(pt3.xMinimum()) + '],[' + str(pt3.yMaximum()) + ',' + str(pt3.xMaximum()) +']]'
					print bounds2
					with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f5_raster:
						
						new_obj = """
				var img_""" + re.sub('[\W_]+', '', i.name()) + """= '""" + out_raster_name + """';
				var img_bounds_""" + re.sub('[\W_]+', '', i.name()) + """ = """+ bounds2 + """;
				var overlay_""" + re.sub('[\W_]+', '', i.name()) + """ = new L.imageOverlay(img_""" + re.sub('[\W_]+', '', i.name()) + """, img_bounds_""" + re.sub('[\W_]+', '', i.name()) + """).addTo(map);
				raster_group.addLayer(overlay_""" + re.sub('[\W_]+', '', i.name()) + """);"""

						f5_raster.write(new_obj)
						f5_raster.close()
	# let's add layer control
	controlStart = """
	L.control.layers({},{"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f6:
		f6.write(controlStart)
		f6.close()

	for i in allLayers: 
		for j in layer_list:
			if i.type() == 0:
				if re.sub('[\W_]+', '', i.name()) == re.sub('[\W_]+', '', j):
					with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f7:
						new_layer = '"' + re.sub('[\W_]+', '', i.name()) + '"' + ": exp_" + re.sub('[\W_]+', '', i.name()) + """JSON,"""
						f7.write(new_layer)
						f7.close()
			elif i.type() == 1:
				if re.sub('[\W_]+', '', i.name()) == re.sub('[\W_]+', '', j):
					with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f7:
						new_layer = '"' + re.sub('[\W_]+', '', i.name()) + '"' + ": overlay_" + re.sub('[\W_]+', '', i.name()) + ""","""
						f7.write(new_layer)
						f7.close()	
	controlEnd = "}).addTo(map);"	
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'rb+') as f8:
		f8.seek(-1, os.SEEK_END)
		f8.truncate()
		f8.write(controlEnd)
		f8.close()
	if opacity_raster == True:
		opacityStart = """
		function updateOpacity(value) {
		"""
		with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f9:
			f9.write(opacityStart)
			f9.close()

		for i in allLayers: 
			for j in layer_list:
				if i.type() == 1:
					if re.sub('[\W_]+', '', i.name()) == re.sub('[\W_]+', '', j):
						with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f10:
							new_opc = """
							overlay_""" + re.sub('[\W_]+', '', i.name()) + """.setOpacity(value);"""
							f10.write(new_opc)
							f10.close()	
		opacityEnd = """}"""	
		with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'rb+') as f11:
			f11.seek(-1, os.SEEK_END)
			f11.truncate()
			f11.write(opacityEnd)
			f11.close()
	elif opacity_raster == False:
		print "no opacity control added"
	
	# let's close the file but ask for the extent of all layers if the user wants to show only this extent:
	if extent == 'layer extent':
		end = """
		map.fitBounds(feature_group.getBounds());
		window.onload = init;
	</script>
</body>
</html>
	"""
	if extent == 'canvas extent':
		end = """
		window.onload = init;
	</script>
</body>
</html>
	"""
	with open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html', 'a') as f12:
		f12.write(end)
		f12.close()
	webbrowser.open(os.path.join(os.getcwd(),outputProjectFileName) + os.sep + 'index.html')
