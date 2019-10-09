var dataset = ee.ImageCollection('MODIS/006/MCD64A1')
    .filter(ee.Filter.date('2000-11-01', '2005-11-01'));
var burnedArea = dataset.select('BurnDate');
var usa_burn = burnedArea.toBands();

var usa_region = ee.Geometry.Polygon([
    [-122.90, 48.49],
    [-122.90, 43.99],
    [-124.75, 43.99],
    [-124.75, 48.49]
]);

Export.image.toDrive({
    image: usa_burn,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'usa_burndate_2000_2005',
    region: usa_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});