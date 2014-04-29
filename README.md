## Synopsis

This plugin provide an easy way to distribute and show your qgis work as a leaflet webmap. 

## Usage

Your current QGIS project helds different data: vector, raster or plugin layers. QGIS2leaf exports the vector layer to GeoJSON and creates a basic webmap from it with the current leaflet version 0.7.2.

## Installation

* Download the source and place it in the `/.qgis2/python/plugins/qgis2leaf` folder  
  (Windows: `C:\Users\{username}\.qgis\python\plugins\qgis2leaf`)
* Import the plugin using the normal add plugin method described [here](http://www.qgis.org/en/docs/user_manual/plugins/plugins.html#managing-plugins 'qgis plugins').

## Version_changes

* 2014-04-22: initial commit
* 2014-04-23: added disambiguation of layer types to avoid break of loop.

## Tests

you may find testdata in the "test_data" folder.
It was tested on Linux Mint.

## Contributors

Currently we are working on this project as part of the blog [digital-geography.com](http://www.digital-geography.com 'digital-geography') and [geolicious.](http://www.geolicious.de 'geolicious')

## License

```
/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
```

