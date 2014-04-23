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
 This script initializes the plugin, making it known to QGIS.
"""
def name():
    return "QGIS2leaf"


def description():
    return "QGIS to leaflet export for several layers"


def version():
    return "Version 0.2"


def icon():
    return "logo.png"


def qgisMinimumVersion():
    return "2.0"

def author():
    return "Riccardo Klinger"

def email():
    return "riccardo.klinger@ggeolicious.de"
    
def classFactory(iface):
    # load qgis2leaf class from file qgis2leaf
    from qgis2leaf import qgis2leaf
    return qgis2leaf(iface)
