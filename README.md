## Synopsis

This plugin provides an easy way to distribute and show your qgis work as a leaflet webmap. 

## Usage

Your current QGIS project helds different data: vector, raster or plugin layers. QGIS2leaf exports the vector layer to GeoJSON and creates a basic webmap from it with the current leaflet version 0.7.2. Additionally we add your raster data as image overlays with a opacity slider.
You can choose between several basemap styles and define the initial extent of the map as well as the dimension of the webmap in your html document. To support big data exports you may disable initial loading of the layers to the map. As the webmap has a layer control you can enable visibility of the layers afterwards.
The popup for features is either a simple table with all your attributes or defined by the attribute `html_exp` in your QGIS vector layer (check `line_feature.shp` in the `test_data` folder). If you want to use a defined symbol in your webmap add an attribute `icon_exp` to your point shapefile and file it wit a relative path on your pc or an html statement. You can define different icons for each feature. Please check index.html of the webmap to customize popup position regarding your chosen icon. You may find testdata in `places_few_1_EPSG3857_categorized.shp` in the `test_data` folder (Donkey designed by Gabriele Malaspina from the thenounproject.com).
For single, categorized and graduated symbol point feature layers we are exporting radius (not for polygons), color and opacity. Unfortunately the export of forms and svg is not embedded at the moment.

## Installation

* Download the source and place it in the `/.qgis2/python/plugins/qgis2leaf` folder  
  (Windows: `C:\Users\{username}\.qgis\python\plugins\qgis2leaf`)
* Import the plugin using the normal "add plugin" method described [here](http://www.qgis.org/en/docs/user_manual/plugins/plugins.html#managing-plugins 'qgis plugins').

## Version_changes
* 2014/08/06 v.0.961: webmap title creation option, improved layer control with pretty names with help from [tomchadwin](https://github.com/tomchadwin) and supported by [the city of Ottawa](http://www.spcottawa.on.ca/)
* 2014/07/11 v.0.96: cluster support, autohotlinking, wfs and wms support and layer order fix with a lot of help from [tomchadwin](https://github.com/tomchadwin)
* 2014/05/22 v.0.95: raster support for image overlays with thanks to https://github.com/geohacker/leaflet-opacity
* 2014/05/22 v.0.9: support for styles of polygons and polylines
* 2014/05/18 v.0.8.4: define your icon for point shapes, new cdn for the needed javascripts
* 2014/05/15 v.0.8.3: style export for graduated, single and categorized symbol point shapefiles
* 2014/05/15 v.0.8.2: style export for graduated and single symbol point shapefiles.
* 2014-05-03 v.0.8.1: new popup creation possibilities
* 2014-05-03 v.0.8: new logo, new UI: toggle visibility
* 2014-05-01 v.0.7: new layer list control for export, non-ascii character encoding problem solved, fixed folder deletion problem, fixed problem with layer names starting with numbers
* 2014-04-27 v.0.6: fixed installation issues for older python versions (thanks to [mlaloux](https://github.com/mlaloux)), enhanced list of basemap-providers (thanks to [leaflet-providers](https://github.com/leaflet/extras/leaflet-providers/))
* 2014-04-26 v.0.5: new control for full map support, optimized UI (thanks to [mtravis](https://github.com/mtravis), correct attribution for basemaps, new css file creation
* 2014-04-25 v.0.4: new layer control for features (thanks to [RCura](https://github.com/RCura)), new GUI with extent setting possibility
* 2014-04-24 v.0.3: new ui with dimension choice for webmap, enhanced html structure for better readability
* 2014-04-23 v.0.2: added disambiguation of layer types to avoid break of loop.
* 2014-04-22: initial commit

## Tests

You may find testdata in the "test_data" folder.
It was tested on Linux Mint and Windows 7 with QGIS 2.2 and 2.4 and Python 2.7.5+ 

## Contributors

Currently we are working on this project as part of the blog [digital-geography.com](http://www.digital-geography.com 'digital-geography') and [geolicious.](http://www.geolicious.de 'geolicious')
You find additional contributors in the changelog.

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

