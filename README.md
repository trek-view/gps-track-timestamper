# GPS Track Timestamper

## In one sentence

Command line Python script that 1) takes a GPX or CSV track (GPS) file, 2) reads existing time data, and 3) writes new time data based on offset values defined by user.

## Why we built this

Some GPS loggers do not report the GPS atomic clock time and instead use the device time (often set by the user). As a result, the GPS times reported in the output can be incorrect.

If you know by how far (number of seconds) the GPS logger is incorrect you can correct it using a time offset.

GPS Track Timestamper gives users a significant amount of flexibility to edit the timestamps in one go using the command line.

_Note: if you need to adjust image date timestamps see [Image Timestamper](https://github.com/trek-view/image-timestamper)._

## How it works

1. You specify a GPS log (GPX or CSV track) with 
2. You define time offset for time values in track
3. The script writes new timestamps into the track.

## The details

### GPX

The script expects `<trkpt>`'s in the following format:

```
<trkpt lat="28.29865" lon="-16.5458055555556">
  <ele>2323.621</ele>
  <time>2019-11-23T10:34:48Z</time>
</trkpt>
```

If a `<trkpt>` has any empty time values, that point will be ignored and the script will continue. For example, we've observed some GPS loggers report GPX docs with objects:

```
<trkpt lat="51.2485" lon="-0.7824">
</trkpt>
```

The script will tell you how many points have been adjusted and how many have been skipped upon completion.

The script will only update `<time>` objects.

### CSV

The script expects header rows of `.csv` files to contain a `GPSDateTime` heading:

```
filename,GPSDateTime
photo_0001.jpg,2020:06:29 18:00:50Z
```

The script also watches for `GPSTimeStamp` and `GPSDateStamp` values:

```
filename,GPSTimeStamp,GPSDateStamp,GPSDateTime
photo_0001.jpg,18:00:50,2020:06:29,2020:06:29 18:00:50Z
```

These two values will also be updated on script output in addition to `GPSDateTime`.

Any other columns in the `.csv` file will be copied to new output and remain unchanged.

## Requirements

### OS Requirements

Works on Windows, Linux and MacOS.

### Software Requirements

* Python version 3.6+
* [Gpxpy](https://pypi.org/project/gpxpy/): python -m pip install gpxpy

## Usage

```
python gps-timestamper.py -o [offset] [INPUT_FILE_PATH] [OUTPUT_DIRECTORY]
```

* offset (`-o`)
	 - Offset (in seconds) from current time values in track file. Can be positive or negative. For example, if the time on the GPS is incorrect by +1 hour (value reported is actually 1 hour ahead of actual capture time) the offset would be -3600. If it was 1 hour behind, the offset would be +3600.

## Output

The new gps track file will be outputted in specified directory with adjusted time values based on offset defined. The file will be outputted in the same format as the input (e.g. `.csv` > `.csv`).

## Quick start 

_Note for MacOS / Unix users_

Remove the double quotes (`"`) around any directory path shown in the examples. For example `"OUTPUT_1"` becomes `OUTPUT_1`.

**Take a GPX file (`INPUT/0001.gpx`) and subtract 5 minutes from all reported `<time>` values then output (to directory `OUTPUT_1`)**

```
python gps-timestamper.py -o -300 "INPUT/0001.gpx" "OUTPUT_1"
```

**Take a CSV file (`INPUT/0001.csv`) and add 45 seconds onto all reported `GPSTimeStamp`, `GPSDateStamp`, and `GPSDateTime` then output (to directory `OUTPUT_2`)**

```
python gps-timestamper.py -o -45 "INPUT/0001.gpx" "OUTPUT_2"
```

## Support 

We offer community support for all our software on our Campfire forum. [Ask a question or make a suggestion here](https://campfire.trekview.org/c/support/8).

## License

GPS Track Timestamper is licensed under a [GNU AGPLv3 License](/LICENSE.txt).