#!/usr/bin/env python

"""
@file datafiles.py
@author Paul Hubbard
@date 7/14/10
@brief Data file routines for MicroSet
"""
import os
import datetime

class MSDatafile():
    """
    Wrapper class for datafiles. Idea is to encapsulate headers and such,
    with an eye out for later changing save formats.
    """
    def __init__(self, filename, vph, data_dir=None, watch_url=None):
        if data_dir:
            self.filename = data_dir + '/' + filename
        else:
            self.filename = filename

        if watch_url:
            self.watch_url = watch_url

        self.vph = vph
        self.fh = open(self.filename, 'w')
        self.write_fileheader()

    def close(self):
        return self.fh.close()

    def flush(self):
        return self.fh.flush()

    def write_beat_error(self, time, reading):
        self.fh.write('%f\t\t%f\n' % (time, reading))
        self.fh.flush()

    def write_rate_error(self, time, rate, error):
        self.fh.write('%f\t%f\t%f\n' % (time, error, rate))
        self.fh.flush()

    def write_fileheader(self):
        buf = []
        rn = datetime.date.today()

        buf.append('Filename: %s' % self.filename)
        buf.append('Vibrations per hour: %d' % self.vph)
        if hasattr(self, 'watch_url'):
            buf.append('Watch info at: ' + self.watch_url)
        buf.append('Copyright Paul Hubbard (phubbard@watchotaku.com) %d' % rn.year)
        buf.append('License: http://creativecommons.org/licenses/by/3.0/us/')
        buf.append('See http://watchotaku.com')
        buf.append('Timestamp: %s' % datetime.datetime.now())
        buf.append('UTC timestamp: %s' % datetime.datetime.utcnow())
        buf.append('')
        buf.append('Time(seconds)\tBeat error\tRate')

        for line in buf:
            self.fh.write(line)
            self.fh.write(os.linesep)
