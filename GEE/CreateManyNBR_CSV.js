//######################################################################################################## 
//#                                                                                                    #\\
//#                      LANDTRENDR SOURCE AND FITTING PIXEL TIME SERIES PLOTTING                      #\\
//#                                                                                                    #\\
//########################################################################################################



//########################################################################################################
//##### INPUTS ##### 
//########################################################################################################


// define function to calculate a spectral index to segment with LT
var segIndex = function(img) {
    var index = img.normalizedDifference(['B4', 'B7']) // calculate normalized difference of band 4 and band 7 (B4-B7)/(B4+B7)
        .multiply(1000) // ...scale results by 1000 so we can convert to int and retain some precision
        .select([0], ['NBR']) // ...name the band
        .set('system:time_start', img.get('system:time_start')); // ...set the output system:time_start metadata to the input image time_start otherwise it is null
    return index;
};

var distDir = -1; // define the sign of spectral delta for vegetation loss for the segmentation index - 
// NBR delta is negetive for vegetation loss, so -1 for NBR, 1 for band 5, -1 for NDVI, etc


// define the segmentation parameters:
// reference: Kennedy, R. E., Yang, Z., & Cohen, W. B. (2010). Detecting trends in forest disturbance and recovery using yearly Landsat time series: 1. LandTrendr—Temporal segmentation algorithms. Remote Sensing of Environment, 114(12), 2897-2910.
//            https://github.com/eMapR/LT-GEE
var run_params = {
    maxSegments: 12,
    spikeThreshold: 0.01,
    vertexCountOvershoot: 20,
    preventOneYearRecovery: true,
    recoveryThreshold: 1,
    pvalThreshold: 0.01,
    bestModelProportion: 0.3,
    minObservationsNeeded: 6
};

//########################################################################################################



//########################################################################################################
//##### ANNUAL SR TIME SERIES COLLECTION BUILDING FUNCTIONS ##### 
//########################################################################################################

//----- MAKE A DUMMY COLLECTOIN FOR FILLTING MISSING YEARS -----
var dummyCollection = ee.ImageCollection([ee.Image([0, 0, 0, 0, 0, 0]).mask(ee.Image(0))]); // make an image collection from an image with 6 bands all set to 0 and then make them masked values


//------ L8 to L7 HARMONIZATION FUNCTION -----
// slope and intercept citation: Roy, D.P., Kovalskyy, V., Zhang, H.K., Vermote, E.F., Yan, L., Kumar, S.S, Egorov, A., 2016, Characterization of Landsat-7 to Landsat-8 reflective wavelength and normalized difference vegetation index continuity, Remote Sensing of Environment, 185, 57-70.(http://dx.doi.org/10.1016/j.rse.2015.12.024); Table 2 - reduced major axis (RMA) regression coefficients
var harmonizationRoy = function(oli) {
    var slopes = ee.Image.constant([0.9785, 0.9542, 0.9825, 1.0073, 1.0171, 0.9949]); // create an image of slopes per band for L8 TO L7 regression line - David Roy
    var itcp = ee.Image.constant([-0.0095, -0.0016, -0.0022, -0.0021, -0.0030, 0.0029]); // create an image of y-intercepts per band for L8 TO L7 regression line - David Roy
    var y = oli.select(['B2', 'B3', 'B4', 'B5', 'B6', 'B7'], ['B1', 'B2', 'B3', 'B4', 'B5', 'B7']) // select OLI bands 2-7 and rename them to match L7 band names
        .resample('bicubic') // ...resample the L8 bands using bicubic
        .subtract(itcp.multiply(10000)).divide(slopes) // ...multiply the y-intercept bands by 10000 to match the scale of the L7 bands then apply the line equation - subtract the intercept and divide by the slope
        .set('system:time_start', oli.get('system:time_start')); // ...set the output system:time_start metadata to the input image time_start otherwise it is null
    return y.toShort(); // return the image as short to match the type of the other data
};


//------ RETRIEVE A SENSOR SR COLLECTION FUNCTION -----
var getSRcollection = function(year, startDay, endDay, sensor, aoi) {
    // get a landsat collection for given year, day range, and sensor
    var srCollection = ee.ImageCollection('LANDSAT/' + sensor + '/C01/T1_SR') // get surface reflectance images
        .filterBounds(aoi) // ...filter them by intersection with AOI
        .filterDate(year + '-' + startDay, year + '-' + endDay); // ...filter them by year and day range

    // apply the harmonization function to LC08 (if LC08), subset bands, unmask, and resample           
    srCollection = srCollection.map(function(img) {
        var dat = ee.Image(
            ee.Algorithms.If(
                sensor == 'LC08', // condition - if image is OLI
                harmonizationRoy(img.unmask()), // true - then apply the L8 TO L7 alignment function after unmasking pixels that were previosuly masked (why/when are pixels masked)
                img.select(['B1', 'B2', 'B3', 'B4', 'B5', 'B7']) // false - else select out the reflectance bands from the non-OLI image
                .unmask() // ...unmask any previously masked pixels 
                .resample('bicubic') // ...resample by bicubic 
                .set('system:time_start', img.get('system:time_start')) // ...set the output system:time_start metadata to the input image time_start otherwise it is null
            )
        );

        // make a cloud, cloud shadow, and snow mask from fmask band
        var qa = img.select('pixel_qa'); // select out the fmask band
        var mask = qa.bitwiseAnd(8).eq(0).and( // include shadow
            qa.bitwiseAnd(16).eq(0)).and( // include snow
            qa.bitwiseAnd(32).eq(0)); // include clouds

        // apply the mask to the image and return it
        return dat.mask(mask); //apply the mask - 0's in mask will be excluded from computation and set to opacity=0 in display
    });

    return srCollection; // return the prepared collection
};


//------ FUNCTION TO COMBINE LT05, LE07, & LC08 COLLECTIONS -----
var getCombinedSRcollection = function(year, startDay, endDay, aoi) {
    var lt5 = getSRcollection(year, startDay, endDay, 'LT05', aoi); // get TM collection for a given year, date range, and area
    var le7 = getSRcollection(year, startDay, endDay, 'LE07', aoi); // get ETM+ collection for a given year, date range, and area
    var lc8 = getSRcollection(year, startDay, endDay, 'LC08', aoi); // get OLI collection for a given year, date range, and area
    var mergedCollection = ee.ImageCollection(lt5.merge(le7).merge(lc8)); // merge the individual sensor collections into one imageCollection object
    return mergedCollection; // return the Imagecollection
};


//------ FUNCTION TO REDUCE COLLECTION TO SINGLE IMAGE PER YEAR BY MEDOID -----
/*
  LT expects only a single image per year in a time series, there are lost of ways to
  do best available pixel compositing - we have found that a mediod composite requires little logic
  is robust, and fast
  
  Medoids are representative objects of a data set or a cluster with a data set whose average 
  dissimilarity to all the objects in the cluster is minimal. Medoids are similar in concept to 
  means or centroids, but medoids are always members of the data set.
*/

// make a medoid composite with equal weight among indices
var medoidMosaic = function(inCollection, dummyCollection) {

    // fill in missing years with the dummy collection
    var imageCount = inCollection.toList(1).length(); // get the number of images 
    var finalCollection = ee.ImageCollection(ee.Algorithms.If(imageCount.gt(0), inCollection, dummyCollection)); // if the number of images in this year is 0, then use the dummy collection, otherwise use the SR collection

    // calculate median across images in collection per band
    var median = finalCollection.median(); // calculate the median of the annual image collection - returns a single 6 band image - the collection median per band

    // calculate the different between the median and the observation per image per band
    var difFromMedian = finalCollection.map(function(img) {
        var diff = ee.Image(img).subtract(median).pow(ee.Image.constant(2)); // get the difference between each image/band and the corresponding band median and take to power of 2 to make negatives positive and make greater differences weight more
        return diff.reduce('sum').addBands(img); // per image in collection, sum the powered difference across the bands - set this as the first band add the SR bands to it - now a 7 band image collection
    });

    // get the medoid by selecting the image pixel with the smallest difference between median and observation per band 
    return ee.ImageCollection(difFromMedian).reduce(ee.Reducer.min(7)).select([1, 2, 3, 4, 5, 6], ['B1', 'B2', 'B3', 'B4', 'B5', 'B7']); // find the powered difference that is the least - what image object is the closest to the median of teh collection - and then subset the SR bands and name them - leave behind the powered difference band
};


//------ FUNCTION TO APPLY MEDOID COMPOSITING FUNCTION TO A COLLECTION -------------------------------------------
var buildMosaic = function(year, startDay, endDay, aoi, dummyCollection) { // create a temp variable to hold the upcoming annual mosiac
    var collection = getCombinedSRcollection(year, startDay, endDay, aoi); // get the SR collection
    var img = medoidMosaic(collection, dummyCollection) // apply the medoidMosaic function to reduce the collection to single image per year by medoid 
        .set('system:time_start', (new Date(year, 8, 1)).valueOf()); // add the year to each medoid image - the data is hard-coded Aug 1st 
    return ee.Image(img); // return as image object
};


//------ FUNCTION TO BUILD ANNUAL MOSAIC COLLECTION ------------------------------
var buildMosaicCollection = function(startYear, endYear, startDay, endDay, aoi, dummyCollection) {
    var imgs = []; // create empty array to fill
    for (var i = startYear; i <= endYear; i++) { // for each year from hard defined start to end build medoid composite and then add to empty img array
        var tmp = buildMosaic(i, startDay, endDay, aoi, dummyCollection); // build the medoid mosaic for a given year
        imgs = imgs.concat(tmp.set('system:time_start', (new Date(i, 8, 1)).valueOf())); // concatenate the annual image medoid to the collection (img) and set the date of the image - hard coded to the year that is being worked on for Aug 1st
    }
    return ee.ImageCollection(imgs); // return the array img array as an image collection
};


//########################################################################################################
//##### FUNCTIONS FOR EXTRACTING AND PLOTTING A PIXEL TIME SERIES ##### 
//########################################################################################################

// ----- FUNCTION TO GET LT DATA FOR A PIXEL -----
var getPoint = function(img, geom, z) {
    return img.reduceRegion({
        reducer: 'first',
        geometry: geom,
        scale: z
    }).getInfo();
};


// ----- FUNCTION TO CHART THE SOURCE AND FITTED TIME SERIES FOR A POINT -----
var chartPoint = function(lt, pt, distDir) {
    Map.centerObject(pt, 14);
    Map.addLayer(pt, { color: "FF0000" });
    var point = getPoint(lt, pt, 10);
    var data = [
        ['x', 'y-original', 'y-fitted']
    ];
    for (var i = 0; i <= (endYear - startYear); i++) {
        data = data.concat([
            [point.LandTrendr[0][i], point.LandTrendr[1][i] * distDir, point.LandTrendr[2][i] * distDir]
        ]);
    }
    for (var i = 0; i <= (endYear - startYear + 1); i++) {
        print(data[i][0] + ',' + data[i][1] + ',' + data[i][2]);
    }
};
//数据存储为列表

var returnImg = function(img) {
    return img.multiply(distDir).set('system:time_start', img.get('system:time_start'))
}


//########################################################################################################
//##### BUILD COLLECTION AND RUN LANDTRENDR #####
//########################################################################################################

// enter longitude and latitude for a point...
// you can get these by first activating the "Inspector" tab...
// then click a location on the map...
// the point coordinates will appear in the at the top...
// of the "Inspector" panel - copy and paste values

//经纬度定义

// define years and dates to include in landsat image collection
var startYear = 1985; // what year do you want to start the time series 
var endYear = 2015; // what year do you want to end the time series
var startDay = '06-01'; // what is the beginning of date filter | month-day
var endDay = '09-30'; // what is the end of date filter | month-day

//long -123.383:-123.319
//lat 45.275:45.313

var longlist = [-124.7, -124.7, -124.7, -124.72, -124.72, -124.71, -124.71, -124.72, -124.7, -124.71, -124.7, -124.72, -124.71, -124.7, -124.72, -124.7, -124.7, -124.71, -124.72, -124.72, -124.72, -124.72, -124.72, -124.71, -124.71, -124.72, -124.7, -124.72, -124.7, -124.71, -124.71, -124.71, -124.71, -124.7, -124.71, -124.71, -124.71, -124.72, -124.72, -124.71, -124.72, -124.71, -124.72, -124.72, -124.71, -124.71, -124.7, -124.71, -124.7, -124.7]
var latlist = [48.23, 48.27, 48.0, 46.26, 45.86, 45.54, 46.81, 45.82, 44.78, 48.32, 46.6, 45.73, 46.34, 46.67, 45.21, 45.51, 47.29, 47.12, 47.67, 44.58, 47.08, 47.79, 48.21, 48.29, 48.13, 48.07, 45.21, 45.12, 47.8, 46.22, 45.11, 46.14, 45.98, 47.14, 47.41, 46.44, 44.37, 46.23, 46.79, 45.78, 44.89, 46.8, 45.07, 45.62, 44.07, 45.09, 44.68, 47.17, 45.14, 44.24]

for (var j = 0; j < 50; j += 1) {
    //----- BUILD LT COLLECTION -----
    // build annual surface reflection collection
    var long = longlist[j]
    var lat = latlist[j]
    var aoi = ee.Geometry.Point(long, lat);
    var annualSRcollection = buildMosaicCollection(startYear, endYear, startDay, endDay, aoi, dummyCollection); // put together the cloud-free medoid surface reflectance annual time series collection

    // apply the function to calculate the segmentation index and adjust the values by the distDir parameter - flip index so that a vegetation loss is associated with a postive delta in spectral value
    var ltCollection = annualSRcollection.map(segIndex) // map the function over every image in the collection - returns a 1-band annual image collection of the spectral index
        .map(returnImg); // ...set the output system:time_start metadata to the input image time_start otherwise it is null

    //----- RUN LANDTRENDR -----
    run_params.timeSeries = ltCollection; // add LT collection to the segmentation run parameter object
    var lt = ee.Algorithms.TemporalSegmentation.LandTrendr(run_params); // run LandTrendr spectral temporal segmentation algorithm

    //----- PLOT THE SOURCE AND FITTED TIME SERIES FOR THE GIVEN POINT -----
    print('A' + long + ',' + lat);
    chartPoint(lt, aoi, distDir); // plot the x-y time series for the given point
}