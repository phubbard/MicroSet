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
    def __init__(self, filename, data_dir=None, watch_url=None):
        if data_dir:
            self.filename = data_dir + '/' + filename
        else:
            self.filename = filename

        if watch_url:
            self.watch_url = watch_url

        self.fh = open(self.filename, 'w')
        self.write_fileheader()

    def close(self):
        return self.fh.close()

    def flush(self):
        return self.fh.flush()

    def write_beat_error(self, time, reading):
        pass

    def write_rate_error(self, time, rate, error):
        pass

    def write_datum(self, time, reading):
        self.fh.write('%f\t%f' % (time, reading))
        self.fh.write(os.linesep)

    def write_fileheader(self):
        buf = []
        rn = datetime.date.today()

        buf.append('Filename: %s' % self.filename)
        if self.watch_url:
            buf.append('Watch info at: ' + self.watch_url)
        buf.append('Copyright Paul Hubbard (phubbard@watchotaku.com) %d' % rn.year)
        buf.append('License: http://creativecommons.org/licenses/by/3.0/us/')
        buf.append('See http://watchotaku.com')
        buf.append('Timestamp: %s' % datetime.datetime.now())
        buf.append('UTC timestamp: %s' % datetime.datetime.utcnow())
        buf.append('')
        buf.append('Time(seconds)\tLux')

        for line in buf:
            self.fh.write(line)
            self.fh.write(os.linesep)