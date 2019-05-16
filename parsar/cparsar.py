from datetime import datetime, timedelta
import os
import sys


ENOENT, EMEDIUMTYPE = range(-1, -3, -1)
PY3 = sys.version_info[0] == 3

##############################################################################
# Copied from:
# http://eli.thegreenplace.net/2011/10/19/perls-guess-if-file-is-text-or-binary-implemented-in-python
##############################################################################

# A function that takes an integer in the 8-bit range and returns
# a single-character byte object in py3 / a single-character string
# in py2.
#
int2byte = (lambda x: bytes((x,))) if PY3 else chr


def istextfile(block):
    """ Uses heuristics to guess whether the given file is text or binary,
        by reading a single block of bytes from the file.
        If more than 30% of the chars in the block are non-text, or there
        are NUL ('\x00') bytes in the block, assume this is a binary file.
    """
    if b'\x00' in block:
        # Files with null bytes are binary
        return False
    elif not block:
        # An empty file is considered a valid text file
        return True

    _text_characters = (
        b''.join(int2byte(i) for i in range(32, 127)) +
        b'\n\r\t\f\b'
    )
    # Use translate's 'deletechars' argument to efficiently remove all
    # occurrences of _text_characters from the block
    nontext = block.translate(None, _text_characters)
    return float(len(nontext)) / len(block) <= 0.30


def parse_date(startdate_str):
    """parse the date SAR collection started"""
    formats = ['%y-%m-%d', '%Y-%m-%d', '%m/%d/%Y', '%d/%m/%Y']
    for fmt in formats:
        try:
            startdate = datetime.strptime(startdate_str, fmt)
            return startdate
        except ValueError:
            continue
    else:  # pylint: disable=W0120
        raise Exception('Unknown date format: %s' % startdate_str)


def format_time(startdate, timestr, afternoon):
    """format the timstr as a datetime str"""
    datetime_str = '%s-%s-%s %s %s' % (startdate.year, startdate.month,
                                       startdate.day, timestr, afternoon)
    timedate = datetime.strptime(datetime_str, '%Y-%m-%d %I:%M:%S %p')
    return datetime.strftime(timedate, '%Y-%m-%dT%H:%M:%S')


def parsefile(filename, section, stats, key=''):
    """parses <filename>, pulling out SAR data corresponding to <section>
    and <stats>"""
    retvals = []
    headermap = None

    if not os.path.exists(filename):
        return ENOENT

    def getstatsline():
        retstr = format_time(startdate, vals[0], vals[1])
        for stat in stats:
            retstr += ',%s' % vals[headermap[stat]]

        return retstr

    with open(filename, 'r') as _file:
        headerstr = ','.join(['#Time'] + stats)
        retvals.append(headerstr)

        header = _file.readline()
        if not istextfile(header[:512]):
            return EMEDIUMTYPE

        header = header.split()
        startdate = parse_date(header[3])
        starttime = None
        starthour = None

        key1, key2 = section.split('|')
        pm = False
        for line in _file:
            if line == '\n' or 'Average' in line or 'Summary' in line:
                continue

            if not starttime and key1 not in line:
                continue

            vals = line.split()

            # keep track of date roll over
            if vals[1] == 'PM':
                if not pm:
                    pm = True
            elif vals[1] == 'AM' and pm:
                startdate = startdate + timedelta(days=1)
                pm = False

            if not starttime and (key1 != vals[2] and key2 != vals[3]):
                continue

            if not starttime:
                starttime = vals[0]
                starthour = vals[1]
                headermap = {n: idx for (idx, n) in enumerate(vals)}
                continue

            if vals[0] == starttime and vals[1] == starthour and len(retvals) > 2:
                return retvals

            if starttime:
                if not key:
                    retvals.append(getstatsline())
                elif vals[2] == key:
                    retvals.append(getstatsline())

    return retvals
