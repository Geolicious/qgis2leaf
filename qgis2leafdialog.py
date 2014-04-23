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
# create the dialog for zoom to point


class qgis2leafDialog(QtGui.QDialog):
	def __init__(self):
		QtGui.QDialog.__init__(self)
        # Set up the user interface from Designer.
		self.ui = Ui_qgis2leaf()
		self.ui.setupUi(self)

		self.setWindowTitle("QGIS2Leaflet")
		
		# Additional code
		#self.inFileName = None
		self.outFileName = None
		self.rasterBands = 0
		
		# For now disable some features
		self.ui.lineEdit_2.setReadOnly(False)
		#self.ui.comboBox.setDisabled(True)
		self.ui.okButton.setDisabled(True)
		
		# Connect signals
		#self.ui.cancelButton.clicked.connect(self.close)
		self.ui.cancelButton.clicked.connect(self.close)
		attrFields = ['OSM Standard', 'OSM Black & White', 'Stamen Toner']
		self.ui.comboBox.addItems(attrFields)

		#self.ui.pushButton.clicked.connect(self.showOpenDialog)
		self.ui.pushButton_2.clicked.connect(self.showSaveDialog)
		self.ui.okButton.clicked.connect(self.export2leaf)

		
	#def showOpenDialog(self):
		#self.inFileName = str(QtGui.QFileDialog.getOpenFileName(self, "Project Name:"))	
		#driver = osgeo.ogr.GetDriverByName('ESRI Shapefile') # will select the driver foir our shp-file creation.
		#shapeData = ogr.Open(str(self.inFileName), 1)
		#self.ui.lineEdit.clear()
		#self.ui.lineEdit.setText(self.inFileName)
		
	def showSaveDialog(self):
		self.outFileName = str(QtGui.QFileDialog.getExistingDirectory(self, "Output Project Name:"))
		
		if self.outFileName != None:
			self.ui.okButton.setDisabled(False)
		self.ui.lineEdit_2.clear()
		self.ui.lineEdit_2.setText(self.outFileName)
		
	def export2leaf(self):
		self.basemapName = self.ui.comboBox.currentText()
		qgis2leaf_exec(self.outFileName, self.basemapName)
		self.close()
