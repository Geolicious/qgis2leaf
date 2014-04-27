# -*- coding: utf-8 -*-
"""
/***************************************************************************
 qgis2leaf
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
# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources_rc
# Import the code for the dialog
from qgis2leafdialog import qgis2leafDialog
import os.path


class qgis2leaf:

	def __init__(self, iface):
		# Save reference to the QGIS interface
		self.iface = iface
		# initialize plugin directory
		self.plugin_dir = os.path.dirname(__file__)
		# initialize locale
		locale = QSettings().value("locale/userLocale")[0:2]
		#localePath = os.path.join(self.plugin_dir, 'i18n', 'qgis2leaf_{}.qm'.format(locale))
		localePath = os.path.join(self.plugin_dir, 'i18n', 'realcentroid_{0}.qm'.format(locale))

		if os.path.exists(localePath):
			self.translator = QTranslator()
			self.translator.load(localePath)

			if qVersion() > '4.3.3':
				QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
		self.dlg = qgis2leafDialog()

	def initGui(self):
    	# Create action that will start plugin configuration
		self.action = QAction(
			QIcon(":/plugins/qgis2leaf/logo.png"),
			u"Exports a QGIS Project to a working leaflet webmap", self.iface.mainWindow())
		# connect the action to the run method
		self.action.triggered.connect(self.run)

		# Add toolbar button and menu item
		self.iface.addToolBarIcon(self.action)
		self.iface.addPluginToWebMenu(u"&qgis2leaf", self.action)

	def unload(self):
		# Remove the plugin menu item and icon
		self.iface.removePluginMenu(u"&qgis2leaf", self.action)
		self.iface.removeToolBarIcon(self.action)

	# run method that performs all the real work
	def run(self):
		# show the dialog
		self.dlg.show()
		# Run the dialog event loop
		self.dlg.exec_()
