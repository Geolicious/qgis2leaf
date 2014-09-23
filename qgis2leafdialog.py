# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgis2leafDialog
                                 A QGIS plugin
 Exports a QGIS Project to a working leaflet webmap
                             -------------------
        begin                : 2014-04-20
        copyright            : (C) 2014 by Riccardo Klinger, Geolicious
        email                : riccardo.klinger@geolicious.de
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

from PyQt4 import QtCore, QtGui
from ui_qgis2leaf import Ui_qgis2leaf
import osgeo.ogr
from osgeo import ogr 
from qgis2leaf_exec import qgis2leaf_exec
from qgis.core import *
from qgis2leaf_layerlist import layerlist
import qgis.utils
import re
import os
import csv
import tempfile

class qgis2leafDialog(QtGui.QDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
		self.ui = Ui_qgis2leaf()
		self.ui.setupUi(self)

		self.setWindowTitle("QGIS 2 Leaflet")
		
		# Additional code
		self.outFileName = None
		self.ui.listWidget.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
				
		# For now disable some features
		self.ui.lineEdit_2.setReadOnly(False)
		self.ui.okButton.setDisabled(False)
		self.ui.listWidget.clear()
		
		# Connect signals
		self.ui.cancelButton.clicked.connect(self.close)
		dictionary = layerlist()
		attrFields = []
		for i in range(len(dictionary)):
			#print dictionary[i]
			for key in dictionary[i]:
				if key == 'META':
					continue
				else:
					attrFields.append(key)
		
		#attrFields = ['OSM Standard', 'OSM Black & White', 'OSM DE', 'OSM HOT', 'OpenSeaMap', 'Thunderforest Cycle', 'Thunderforest Transport', 'Thunderforest Landscape', 'Thunderforest Outdoors', 'OpenMapSurfer Roads', 'OpenMapSurfer adminb', 'OpenMapSurfer roadsg', 'MapQuestOpen OSM', 'MapQuestOpen Aerial', 'Stamen Terrain','Stamen Toner', 'Stamen Watercolor', 'OpenWeatherMap Clouds', 'OpenWeatherMap Precipitation', 'OpenWeatherMap Rain', 'OpenWeatherMap Pressure','OpenWeatherMap Wind', 'OpenWeatherMap Temp', 'OpenWeatherMap Snow']
		self.ui.comboBox.addItems(attrFields)
		extFields = ['canvas extent', 'layer extent']
		self.ui.comboBox_2.addItems(extFields)
		visFields = ['show all', 'show none']
		self.ui.lineEdit_2.setText(tempfile.gettempdir())
		self.outFileName = self.ui.lineEdit_2.text()
		self.ui.comboBox_3.addItems(visFields)
		self.ui.pushButton_2.clicked.connect(self.showSaveDialog)
		#settings dialog:
		self.ui.lineEdit_3.setText(str(tempfile.gettempdir()) + os.sep +'settings.csv')
		self.SettingsFileName = self.ui.lineEdit_3.text()
		self.ui.lineEdit_4.setText(str(tempfile.gettempdir()) + os.sep +'settings.csv')
		self.SettingsFileNameLoad = self.ui.lineEdit_4.text()
		self.ui.pushButton_3.clicked.connect(self.showSaveDialogSettings)
		self.ui.pushButton_4.clicked.connect(self.showLoadDialogSettings)

		self.ui.okButton.clicked.connect(self.export2leaf)		
		self.ui.okButton_2.clicked.connect(self.SaveDialogSettings)
		self.ui.okButton_3.clicked.connect(self.LoadDialogSettings)
		self.ui.getSizeButton.clicked.connect(self.getSize)
		self.ui.getButton.clicked.connect(self.layerGet)
		# set default width and height for the leaflet output
		self.ui.radioButton.setChecked(False)
		self.full_screen = 0
		self.width = self.ui.width_box.setText('800')
		self.height = self.ui.height_box.setText('600')
		self.ui.radioButton.toggled.connect(self.width_)
		if QgsProject.instance().title() != "":
			self.webpage_name = self.ui.webpage_name.setText(unicode(QgsProject.instance().title()))
			self.webmap_head = self.ui.webmap_head.setText(unicode(QgsProject.instance().title()))
			self.webmap_subhead = self.ui.webmap_subhead.setText(unicode(QgsProject.instance().title()))
		else:
			self.webpage_name = self.ui.webpage_name.setText("QGIS2leaf webmap")
			self.webmap_head = self.ui.webmap_head.setText("This is the title")
			self.webmap_subhead = self.ui.webmap_subhead.setText("This is the subtitle")

	def getSize(self):
		canvas = qgis.utils.iface.mapCanvas()
		canvasSize = canvas.size()    
		canvasWidth = canvasSize.width()
		canvasHeight = canvasSize.height()
		self.width = self.ui.width_box.setText(str(canvasWidth))
		self.height = self.ui.height_box.setText(str(canvasHeight))
	def layerGet(self):
		self.ui.listWidget.clear()
		canvas = qgis.utils.iface.mapCanvas()
		allLayers = canvas.layers()
		for i in allLayers:
			if i.type() == 2:
				print(i.name() + " skipped as it is not a vector layer nor a raster layer")  
			if i.type() == 0: 
				#print i.type()
				layer_granted = 1
				print layer_granted
				fields = i.pendingFields()
				field_names = [field.name() for field in fields]
				for field in field_names:
					m = re.search('[ - ]|[\{-\~]|[^\x00-\x7F]|[ -/]|[=]|[@]|[<]|[>]|[[]|[]]|[\^]',field)
					if str(m) != "None":
						QtGui.QMessageBox.about(self, "Non supported attribute names detected!", "Your layer<br><b>"+ unicode(i.name()) + "</b><br>has an attribute called<br><b>" + unicode(field) + "</b><br>There are characters in the attribute name that are not allowed:<br><b>'" + unicode(m.group(0))+ "'</b><br>Consider using the <a href='http://plugins.qgis.org/plugins/tablemanager/'>table manager plugin</a> to rename your attributes.<br><br><b><em>As it is, this layer will not be exported for the webmap.</em></b>")
						layer_granted = 0
				if layer_granted == 1:
					self.ui.listWidget.addItem(i.name())
			if i.type() == 1:
				self.ui.listWidget.addItem(i.name())
		self.rows = self.ui.listWidget.count()
		self.ui.listWidget.selectAll()
	def width_(self):
		if self.ui.radioButton.isChecked() == True:
			self.width = self.ui.width_box.setText('')
			self.height = self.ui.height_box.setText('')
			self.full_screen = 1
		if self.ui.radioButton.isChecked() != True:
			self.width = self.ui.width_box.setText('800')
			self.height = self.ui.height_box.setText('600')
			self.full_screen = 0
	def showSaveDialog(self):
		self.outFileName = str(QtGui.QFileDialog.getExistingDirectory(self, "Output Project Name:"))
		if self.outFileName != None:
			self.ui.okButton.setDisabled(False)
		self.ui.lineEdit_2.clear()
		self.ui.lineEdit_2.setText(self.outFileName)
	def showLoadDialogSettings(self):
		self.SettingsFileNameLoad = QtGui.QFileDialog.getOpenFileName(self, 'Dialog Title', str(tempfile.gettempdir()) + os.sep + 'settings.csv', '*.csv')
		if self.SettingsFileNameLoad != None:
			self.ui.okButton_3.setDisabled(False)
		self.ui.lineEdit_4.clear()
		self.ui.lineEdit_4.setText(self.SettingsFileNameLoad)
	def showSaveDialogSettings(self):
		self.SettingsFileName = QtGui.QFileDialog.getSaveFileName(self, 'Dialog Title', str(tempfile.gettempdir()) + os.sep + 'settings.csv', '*.csv')
		if self.SettingsFileName != None:
			self.ui.okButton_2.setDisabled(False)
		self.ui.lineEdit_3.clear()
		self.ui.lineEdit_3.setText(self.SettingsFileName)
	# here comes the saving of the dialog	
	def SaveDialogSettings(self):
		import csv
		my_dict = {"test": 1, "testing": 2}
		#here the list of arguments:
		self.basemapname = self.ui.comboBox.currentText()
		self.width = self.ui.width_box.text()
		self.height = self.ui.height_box.text()
		self.webpage_name = self.ui.webpage_name.text()
		self.webmap_head = self.ui.webmap_head.text()
		self.webmap_subhead = self.ui.webmap_subhead.text()
		self.extent = self.ui.comboBox_2.currentText()
		self.visible = self.ui.comboBox_3.currentText()
		self.layer_list = self.ui.listWidget.selectedItems()
		self.opacity = self.ui.checkBox.isChecked()
		self.encode2JSON = self.ui.encode2JSON.isChecked()
		self.createcluster = self.ui.createcluster.isChecked()
		self.legend = self.ui.createlegend.isChecked()
		self.locate = self.ui.locate.isChecked()
		self.address = self.ui.address.isChecked()
		my_settings = {"Foldername": self.outFileName, "Basemap": self.basemapname, "Width": self.width, "Height": self.height, "Extent": self.extent, "Fullscreen": self.full_screen,  "Visibility": self.visible, "Opacity_Control": self.opacity, "Encoding_WFS": self.encode2JSON, "Cluster": self.createcluster, "Webpage_Name": self.webpage_name, "Webmap_Title": self.webmap_head, "Webmap_SubTitle": self.webmap_subhead, "Legend":  self.legend,"Locate": self.locate, "Address": self.address}
		
		with open(str(self.ui.lineEdit_3.text()), 'wb') as f: 
   			w = csv.DictWriter(f, my_settings.keys())
   			w.writeheader()
    			w.writerow(my_settings)
	# here comes the loading of the dialog
	def LoadDialogSettings(self):
		import csv
		
		with open(str(self.ui.lineEdit_4.text()), mode='r') as infile:
   			reader = csv.DictReader(infile)
			for rows in reader:
				#now restore the settings by mapping the file:
				self.ui.lineEdit_2.setText(rows['Foldername'])
				index_basemap = self.ui.comboBox.findText(rows['Basemap'])
				self.ui.comboBox.setCurrentIndex(index_basemap)
				self.ui.width_box.setText(rows['Width'])
				self.ui.height_box.setText(rows['Height'])
				index_extent = self.ui.comboBox_2.findText(rows['Extent'])
				self.ui.comboBox_2.setCurrentIndex(index_extent)
				print rows['Fullscreen']
				if rows['Fullscreen'] == "0":
					print rows['Fullscreen']
					self.ui.radioButton.setChecked(False)
					self.full_screen = 0
					self.width=self.ui.width_box.setText(rows['Width'])
					self.height=self.ui.height_box.setText(rows['Height'])
				if rows['Fullscreen'] == "1":
					print rows['Fullscreen']
					self.ui.radioButton.setChecked(True)
					self.width = self.ui.width_box.setText('')
					self.height = self.ui.height_box.setText('')
					self.full_screen = 1
				index_visibility = self.ui.comboBox_3.findText(rows['Visibility'])
				self.ui.comboBox_3.setCurrentIndex(index_visibility)
				if rows["Opacity_Control"] == "False":
					self.ui.checkBox.setChecked(False)
				if rows["Opacity_Control"] == "True":
					self.ui.checkBox.setChecked(True)
				if rows["Encoding_WFS"] == "False":
					self.ui.encode2JSON.setChecked(False)
				if rows["Encoding_WFS"] == "True":
					self.ui.encode2JSON.setChecked(True)
				if rows["Cluster"] == "False":
					self.ui.createcluster.setChecked(False)
				if rows["Cluster"] == "True":
					self.ui.createcluster.setChecked(True)
				self.ui.webpage_name.setText(rows['Webpage_Name'])
				self.ui.webmap_head.setText(rows['Webmap_Title'])
				self.ui.webmap_subhead.setText(rows['Webmap_SubTitle'])
				if rows["Legend"] == "False":
					self.ui.createlegend.setChecked(False)
				if rows["Legend"] == "True":
					self.ui.createlegend.setChecked(True)
				if rows["Locate"] == "False":
					self.ui.locate.setChecked(False)
				if rows["Locate"] == "True":
					self.ui.locate.setChecked(True)
				if rows["Address"] == "False":
					self.ui.address.setChecked(False)
				if rows["Address"] == "True":
					self.ui.address.setChecked(True)

	def export2leaf(self):
		dictionary = layerlist()
		for i in range(len(dictionary)):
			#print dictionary[i]
			for key in dictionary[i]:
				if key == 'META':
					continue
				else:
					if self.ui.comboBox.currentText() == key:
						self.basemapMeta = dictionary[i]['META']
						self.basemapName = self.ui.comboBox.currentText()
						self.basemapAddress = dictionary[i][self.ui.comboBox.currentText()]
		self.outFileName=self.ui.lineEdit_2.text()		
		self.width = self.ui.width_box.text()
		self.height = self.ui.height_box.text()
		self.webpage_name = self.ui.webpage_name.text()
		self.webmap_head = self.ui.webmap_head.text()
		self.webmap_subhead = self.ui.webmap_subhead.text()
		self.extent = self.ui.comboBox_2.currentText()
		self.visible = self.ui.comboBox_3.currentText()
		self.layer_list = self.ui.listWidget.selectedItems()
		self.opacity = self.ui.checkBox.isChecked()
		self.encode2JSON = self.ui.encode2JSON.isChecked()
		self.createcluster = self.ui.createcluster.isChecked()
		self.legend = self.ui.createlegend.isChecked()
		self.locate = self.ui.locate.isChecked()
		self.address = self.ui.address.isChecked()
		#print self.opacity
		for i in range(len(self.layer_list)): 
			self.layer_list[i] = re.sub('[\W_]+', '', self.layer_list[i].text())
		qgis2leaf_exec(self.outFileName, self.basemapName, self.basemapMeta, self.basemapAddress, self.width, self.height, self.extent, self.full_screen, self.layer_list, self.visible, self.opacity, self.encode2JSON,self.createcluster, self.webpage_name, self.webmap_head,self.webmap_subhead, self.legend,self.locate,self.address)
		self.close()
