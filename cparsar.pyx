from datetime import datetime
import os
import re
import sys


class FileNotFound(Exception):
    """Exception raised when sar file isn't found"""
    pass


def format_time(startdate, timestr, afternoon):
    """format the timstr as a datetime str"""
    timedate = datetime.strptime('%s %s %s' % (startdate, timestr, afternoon),
                                 '%y-%m-%d %I:%M:%S %p')
    return datetime.strftime(timedate, '%Y-%m-%dT%H:%M:%S')


def parsefile(filename, section, stats, key=''):
    """parses <filename>, pulling out SAR data corresponding to <section>
    and <stats>"""
    retvals = []
    headermap = None
    regex = re.compile(r'\s+')

    if not os.path.exists(filename):
        raise FileNotFound('file "%s" does not exist' % filename)

    def getstatsline():
        retstr = format_time(startdate, vals[0], vals[1])
        for stat in stats:
            retstr += ',%f' % float(vals[headermap[stat]])

        return retstr

    with open(filename, 'r') as _file:
        headerstr = ','.join(['#Time'] + stats)
        retvals.append(headerstr)

        header = _file.readline()
        header = regex.sub('|', header).split('|')
        startdate = header[3]
        starttime = None

        for line in _file:
            line = line.strip()
            if not line or 'Average' in line:
                continue

            key1, _ = section.split('|')
            if not starttime and key1 not in line:
                continue

            line = regex.sub('|', line)

            if not starttime and section not in line:
                continue

            vals = line.split('|')
            linetime = vals[0]

            if not starttime:
                starttime = linetime
                headermap = {n: idx for (idx, n) in enumerate(vals)}
                continue

            # TODO: Handle SAR data at 1 minute increments
            if linetime == starttime:
                return retvals

            if starttime:
                statsline = ''
                if key:
                    if vals[2] == key:
                        statsline = getstatsline()
                else:
                    statsline = getstatsline()

                if statsline:
                    retvals.append(statsline)

    return retvals
