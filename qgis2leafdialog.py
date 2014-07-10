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
import qgis.utils
import re
import os
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
		attrFields = ['OSM Standard', 'OSM Black & White', 'OSM DE', 'OSM HOT', 'OpenSeaMap', 'Thunderforest Cycle', 'Thunderforest Transport', 'Thunderforest Landscape', 'Thunderforest Outdoors', 'OpenMapSurfer Roads', 'OpenMapSurfer adminb', 'OpenMapSurfer roadsg', 'MapQuestOpen OSM', 'MapQuestOpen Aerial', 'Stamen Terrain','Stamen Toner', 'Stamen Watercolor', 'OpenWeatherMap Clouds', 'OpenWeatherMap Precipitation', 'OpenWeatherMap Rain', 'OpenWeatherMap Pressure','OpenWeatherMap Wind', 'OpenWeatherMap Temp', 'OpenWeatherMap Snow']
		self.ui.comboBox.addItems(attrFields)
		extFields = ['canvas extent', 'layer extent']
		self.ui.comboBox_2.addItems(extFields)
		visFields = ['show all', 'show none']
		self.ui.lineEdit_2.setText(tempfile.gettempdir())
		self.outFileName = self.ui.lineEdit_2.text()
		self.ui.comboBox_3.addItems(visFields)
		self.ui.pushButton_2.clicked.connect(self.showSaveDialog)
		self.ui.okButton.clicked.connect(self.export2leaf)
		self.ui.getSizeButton.clicked.connect(self.getSize)
		self.ui.getButton.clicked.connect(self.layerGet)
		# set default width and height for the leaflet output
		self.ui.radioButton.setChecked(False)
		self.full_screen = 0
		self.width = self.ui.width_box.setText('800')
		self.height = self.ui.height_box.setText('600')
		self.ui.radioButton.toggled.connect(self.width_)
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
			if i.type() < 2: 
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
		
	def export2leaf(self):
		self.basemapName = self.ui.comboBox.currentText()
		self.width = self.ui.width_box.text()
		self.height = self.ui.height_box.text()
		self.extent = self.ui.comboBox_2.currentText()
		self.visible = self.ui.comboBox_3.currentText()
		self.layer_list = self.ui.listWidget.selectedItems()
		self.opacity = self.ui.checkBox.isChecked()
		self.encode2JSON = self.ui.encode2JSON.isChecked()
		self.createcluster = self.ui.createcluster.isChecked()
		#print self.opacity
		for i in range(len(self.layer_list)): 
			self.layer_list[i] = re.sub('[\W_]+', '', self.layer_list[i].text())
		qgis2leaf_exec(self.outFileName, self.basemapName, self.width, self.height, self.extent, self.full_screen, self.layer_list, self.visible, self.opacity, self.encode2JSON,self.createcluster)
		self.close()