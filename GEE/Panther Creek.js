/**
 * Function to mask clouds based on the pixel_qa band of Landsat SR data.
 * @param {ee.Image} image Input Landsat SR image
 * @return {ee.Image} Cloudmasked Landsat image
 */
var cloudMaskL457 = function(image) {
    var qa = image.select('pixel_qa');
    // If the cloud bit (5) is set and the cloud confidence (7) is high
    // or the cloud shadow bit is set (3), then it's a bad pixel.
    var cloud = qa.bitwiseAnd(1 << 5)
        .and(qa.bitwiseAnd(1 << 7))
        .or(qa.bitwiseAnd(1 << 3));
    // Remove edge pixels that don't occur in all bands
    var mask2 = image.mask().reduce(ee.Reducer.min());
    return image.updateMask(cloud.not()).updateMask(mask2);
};

var dataset = ee.ImageCollection('LANDSAT/LE07/C01/T1_SR')
    .filterDate('2010-08-01', '2010-08-31')
    .map(cloudMaskL457);
var b2 = dataset.select('b2')
var b3 = dataset.select('b3')
var b4 = dataset.select('b4')
var pc = ee.Geometry.Polygon([
    [-123.320503, 45.323427],
    [-123.320503, 45.275370],
    [-123.405647, 45.275370],
    [-123.405647, 45.323427]
])

Export.image.toDrive({
    image: ndvi,
    region: pc,
    scale: 2.5,
    crs: 'EPSG:4326',
    maxPixels: 1e13
});