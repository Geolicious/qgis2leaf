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

		self.setWindowTitle("QGIS 2 Leaflet")
		
		# Additional code
		self.outFileName = None
		self.rasterBands = 0
		
		# For now disable some features
		self.ui.lineEdit_2.setReadOnly(False)
		self.ui.okButton.setDisabled(True)
		
		# Connect signals
		self.ui.cancelButton.clicked.connect(self.close)
		attrFields = ['OSM Standard', 'OSM Black & White', 'Stamen Toner']
		self.ui.comboBox.addItems(attrFields)
		extFields = ['canvas extent', 'layer extent']
		self.ui.comboBox_2.addItems(extFields)
		self.ui.pushButton_2.clicked.connect(self.showSaveDialog)
		self.ui.okButton.clicked.connect(self.export2leaf)
		
		# set default width and height for the leaflet output
		self.ui.radioButton.setChecked(False)
		self.full_screen = 0
		self.width = self.ui.width_box.setText('800')
		self.height = self.ui.height_box.setText('600')
		self.ui.radioButton.toggled.connect(self.width_)
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
		qgis2leaf_exec(self.outFileName, self.basemapName, self.width, self.height, self.extent, self.full_screen)
		self.close()
