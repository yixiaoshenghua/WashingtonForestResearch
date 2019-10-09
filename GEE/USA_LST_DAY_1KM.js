var dataset = ee.ImageCollection('MODIS/006/MOD11A1')
    .filter(ee.Filter.date('2014-07-10', '2014-07-20'));
var landSurfaceTemperature = dataset.select('LST_Night_1km').max();

var usa_region = ee.Geometry.Polygon([
    [-122.90, 48.49],
    [-122.90, 43.99],
    [-124.75, 43.99],
    [-124.75, 48.49]
]);

Export.image.toDrive({
    image: landSurfaceTemperature,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'usa_LST_Night_1km_2014_07_10_2014_07_20',
    region: usa_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});