# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author: hq@trekview.org
# Created: 2020-06-10
# Copyright: Trek View
# Licence: GNU AGPLv3
# -------------------------------------------------------------------------------

import os
import argparse
from pathlib import Path
import xml.sax
import csv
import datetime
import gpxpy
import traceback


def validate_file_type(path):
    """
    Check the file type is csv or xml.
    """
    with open(path, 'rb') as fh:
        try:
            xml.sax.parse(fh, xml.sax.ContentHandler())
            return 'xml'
        except:  # SAX' exceptions are not public
            pass

    try:
        reader = csv.reader(open(path, 'rb'))
        return 'csv'
    except csv.Error:
        pass

    return 'file type is not correct'


def update_gps_track_log(log_path, output_path, offset):
    """
    update log file.
    support gpx and exif csv file.
    """
    file_type = validate_file_type(log_path)
    updated_points = 0
    removed_points = 0

    if file_type == 'file type is not correct':
        return False
    elif file_type == 'csv':
        track_logs = []
        # Parse exif csv file to dict list
        with open(log_path, 'r', encoding='utf8') as log_file:
            reader = csv.DictReader(log_file)
            for i in reader:
                date_time = i.get('GPSDateTime')
                if date_time:
                    new_date_time = datetime.datetime.strptime(date_time, '%Y:%m:%d %H:%M:%SZ') + datetime.timedelta(0, offset)
                    i.update({
                        'GPSDateTime': new_date_time.strftime('%Y:%m:%d %H:%M:%SZ'),
                        'GPSDateStamp': new_date_time.strftime('%Y:%m:%d'),
                        'GPSTimeStamp': new_date_time.strftime('%H:%M:%S')
                    })
                    updated_points += 1
                else:
                    removed_points += 1
                track_logs.append(i)
        with open(output_path, 'w') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=track_logs[0].keys())
            writer.writeheader()
            writer.writerows(track_logs)

    else:
        new_gpx = gpxpy.gpx.GPX()
        with open(log_path, 'r') as gpxfile:
            gpxfile.seek(0)
            try:
                gpx = gpxpy.parse(gpxfile)
                for track in gpx.tracks:
                    gpx_track = gpxpy.gpx.GPXTrack()
                    new_gpx.tracks.append(gpx_track)
                    for segment in track.segments:
                        gpx_segment = gpxpy.gpx.GPXTrackSegment()
                        gpx_track.segments.append(gpx_segment)
                        for point in segment.points:
                            if point.time:
                                gpx_segment.points.append(gpxpy.gpx.GPXTrackPoint(
                                    latitude=point.latitude, longitude=point.longitude, time=point.time + datetime.timedelta(0, offset)))
                                updated_points += 1
                            else:
                                removed_points += 1

            except Exception as e:
                input("""It's not correct GPX file.\n\nPress any key to quit""")
                quit()

        print('Updated Points : {} \n\nRemoved Points: {}'.format(updated_points, removed_points))
        with open(output_path, "w") as f:
            f.write(new_gpx.to_xml())


def update_log(args):
    path = Path(__file__)
    log_path = os.path.abspath(args.input_file)
    output_logo_file = os.path.abspath(args.output_file)
    offset = int(args.offset)

    # Validate log file exist
    if not os.path.isfile(log_path):
        if os.path.isfile(os.path.join(path.parent.resolve(), log_path)):
            log_path = os.path.join(path.parent.resolve(), log_path)
        else:
            input('No valid input file is given!\nInput file {0} or {1} does not exist!'.format(
                os.path.abspath(log_path),
                os.path.abspath(os.path.join(path.parent.resolve(), log_path))))
            input('Press any key to continue')
            quit()

    print('File: {} is reading now.'.format(log_path))

    update_gps_track_log(log_path, output_logo_file, offset)

    input('\nTimestamps successfully updated in new file.\n\nPress any key to quit')
    quit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Image GeoTagger metadata setter')

    parser.add_argument('-o', '--offset',
                        action='store',
                        dest='offset',
                        default=0,
                        help='Offset gps track times')

    parser.add_argument('input_file',
                        action='store',
                        help='Path to input log file.')

    parser.add_argument('output_file',
                        action="store",
                        help='Path to output log file.')

    parser.add_argument('--version',
                        action='version',
                        version='%(prog)s 1.0')

    args = parser.parse_args()

    update_log(args)
