var dataset1 = ee.ImageCollection('IDAHO_EPSCOR/TERRACLIMATE')
    .filter(ee.Filter.date('1990-01-01', '1994-12-31'));
var maximumTemperature1 = dataset1.select('tmmx').max();
var dataset2 = ee.ImageCollection('IDAHO_EPSCOR/TERRACLIMATE')
    .filter(ee.Filter.date('1995-01-01', '1999-12-31'));
var maximumTemperature2 = dataset2.select('tmmx').max();
var dataset3 = ee.ImageCollection('IDAHO_EPSCOR/TERRACLIMATE')
    .filter(ee.Filter.date('2000-01-01', '2004-12-31'));
var maximumTemperature3 = dataset3.select('tmmx').max();
var dataset4 = ee.ImageCollection('IDAHO_EPSCOR/TERRACLIMATE')
    .filter(ee.Filter.date('2005-01-01', '2009-12-31'));
var maximumTemperature4 = dataset4.select('tmmx').max();
var dataset5 = ee.ImageCollection('IDAHO_EPSCOR/TERRACLIMATE')
    .filter(ee.Filter.date('2010-01-01', '2015-12-31'));
var maximumTemperature5 = dataset5.select('tmmx').max();
var usa_region = ee.Geometry.Polygon([
    [-122.90, 48.49],
    [-122.90, 43.99],
    [-124.75, 43.99],
    [-124.75, 48.49]
])
var chn_region = ee.Geometry.Polygon([
    [120.15, 46.66],
    [120.15, 53.57],
    [127.99, 53.57],
    [127.99, 46.66]
])

Export.image.toDrive({
    image: maximumTemperature1,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'usa_Temperature_1990_1995',
    region: usa_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});
Export.image.toDrive({
    image: maximumTemperature2,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'usa_Temperature_1995_2000',
    region: usa_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});
Export.image.toDrive({
    image: maximumTemperature4,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'usa_Temperature_2000_2005',
    region: usa_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});
Export.image.toDrive({
    image: maximumTemperature5,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'usa_Temperature_2005_2010',
    region: usa_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});
Export.image.toDrive({
    image: maximumTemperature3,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'usa_Temperature_2010_2015',
    region: usa_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});
Export.image.toDrive({
    image: maximumTemperature1,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'chn_temperature_1990_1995',
    region: chn_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});
Export.image.toDrive({
    image: maximumTemperature2,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'chn_temperature_1995_2000',
    region: chn_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});
Export.image.toDrive({
    image: maximumTemperature3,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'chn_temperature_2000_2005',
    region: chn_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});
Export.image.toDrive({
    image: maximumTemperature4,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'chn_temperature_2005_2010',
    region: chn_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});
Export.image.toDrive({
    image: maximumTemperature5,
    folder: 'lt-gee_temperature_map',
    fileNamePrefix: 'chn_temperature_2010_2015',
    region: chn_region,
    scale: 30,
    crs: 'EPSG:5070',
    maxPixels: 1e13
});