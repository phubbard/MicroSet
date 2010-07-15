#!/usr/bin/env python

"""
@file MicroSet/main.py
@author Paul Hubbard
@date 7/14/10
@brief Starting from the flexoptometer code, a driver/reader for the microset
watch timer. To start with, just log data to disk.
"""

import sys
import time
import logging

from twisted.protocols.basic import LineReceiver

from twisted.internet import reactor
from twisted.internet.serialport import SerialPort
from twisted.python import usage

from datafiles import MSDatafile

class THOptions(usage.Options):
    optParameters = [
        ['baudrate', 'b', 9600, 'Serial baudrate'],
        ['port', 'p', '/dev/tty.KeySerial1', 'Serial port to use'],
        ['filename', 'f', 'datafile.txt', 'datafile to append to'],
        ['watch_url', 'u', None, 'URL for watch information'],
        ['data_dir', 'd', 'data', 'Datafile directory to write to'],
        ['runtime', 'r', 0, 'Seconds to capture data'],
        ]

class MicroSet(LineReceiver):
    def __init__(self, filename, data_dir=None, run_time=0, watch_url=None):

        self.dfile = MSDatafile(filename, data_dir, watch_url=watch_url)
        logging.debug('Filename: %s ' % self.dfile.filename)
        if run_time > 0:
            logging.debug('Run time: %d seconds' % run_time)
        self.end_time = time.time() + run_time
        self.run_time = run_time

    def connectionMade(self):
        logging.debug('Connection made!')
        self.tzero = time.time()


    def parse_rate_datum(self, strings):
        assert(len(strings) == 2)

        vph = 0.0
        beat_error = 0
        try:
            vph = float(strings[0])
            prefix_str = strings[1][0]
            beat_error = int(strings[1][1:])
        except ValueError, ve:
            logging.exception('Error parsing rate! %s' % ve)
            return None, None

        return vph, beat_error

    def parse_beat_error(self, string):
        assert(len(string) == 1)
        beat_error = 0
        try:
            prefix_str = strings[1][0]
            assert(prefix_str == 'W')
            beat_error = int(strings[1][1:])
        except ValueError, ve:
            logging.exception('Error parsing beat error! %s' % ve)
            return None, None

        return beat_error

    def lineReceived(self, line):
        logging.debug(line)
        ts = time.time() - self.tzero

        try:
            strs = line.strip().split()
        except ValueError, ve:
            logging.exception('Error parsing string; ignored. Error %s' % ve)
            return

        if len(strs) == 0:
            logging.warn('Empty line ignored!')
            return

        if len(strs) == 1:
            logging.info('Looks like beat error data')
            logging.debug(self.parse_beat_error(strs))
        elif len(strs) == 2:
            logging.info('Looks like rate data')
            logging.debug(self.parse_rate_datum(strs))
        else:
            logging.error('Unknown data type - %d fields found!' % len(strs))
            return

        #self.dfile.write_datum(ts, fv)

        if self.run_time > 0:
            if time.time() > self.end_time:
                logging.info('Done.')
                self.dfile.close()
                self.transport.loseConnection()
                reactor.stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, \
                format='%(asctime)s %(levelname)s [%(funcName)s] %(message)s')

    o = THOptions()
    try:
        o.parseOptions()
    except usage.UsageError, errortext:
        logging.error('%s %s' % (sys.argv[0], errortext))
        logging.info('Try %s --help for usage details' % sys.argv[0])
        raise SystemExit, 1

    baudrate = int(o.opts['baudrate'])
    port = o.opts['port']
    filename = o.opts['filename']
    data_dir = o.opts['data_dir']
    run_time = int(o.opts['runtime'])
    watch_url = o.opts['watch_url']

    logging.debug('About to open port %s' % port)
    mset = MicroSet(filename, data_dir=data_dir, run_time=run_time,
                 watch_url=watch_url)
    s = SerialPort(mset, port, reactor, baudrate=baudrate)

    reactor.run()
