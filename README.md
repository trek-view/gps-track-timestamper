# GPS Track Timestamper

Sometimes the time on your GPS logger might be incorrect. If you know by how far (number of seconds) the GPS logger is incorrect you can correct it using a time offset.

Currently the Image Geotagger script allows user to set time offset for GPS track timestamp before stitching into photos https://github.com/trek-view/image-geotagger

We should remove this function from this script and package as a new script in this repo.

This is a useful feature in the (Trek View) pipeline, but makes more sense to be in a separate script to be run before this one.

Users should be able to take track log file formats:

* GPX
* ExifTool .CSV file

And set '-o' (offset gps track times) -- a value in seconds to offset each gps track timestamp. Can be either positive of negative.

Offset should be specified in seconds. For example, if the time on the GPS is incorrect by +1 hour (value reported is actually 1 hour ahead of actual capture time) the offset would be -3600. If it was 1 hour behind, the offset would be +3600.

Note: if you need to adjust `originaldatetime` timestamps see [Image Timestamper](https://github.com/trek-view/image-timestamper).