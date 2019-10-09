var dataset = ee.Image('NASA/ASTER_GED/AG100_003');
var temperature = dataset.select('temperature');

var usa_region = ee.Geometry.Polygon([
    [-122.90, 48.49],
    [-122.90, 43.99],
    [-124.75, 43.99],
    [-124.75, 48.49]
]);

Export.image.toDrive({
    image: temperature,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'usa_temp_2000_2008',
    region: usa_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});