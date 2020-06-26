# GPS Track Timestamper


Currently the Image Geotagger script allows user to set time offset for GPS track timestamp before stitching into photos https://github.com/trek-view/image-geotagger

We should remove this function from this script and package as a new script in this repo.

This is a useful feature in the (Trek View) pipeline, but makes more sense to be in a separate script to be run before this one.

Users should be able to take track log file formats:

* GPX
* ExifTool .CSV file

And set '-o' (offset gps track times) -- a value in seconds to offset each gps track timestamp. Can be either positive of negative.