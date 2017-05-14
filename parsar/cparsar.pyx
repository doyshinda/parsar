from datetime import datetime, timedelta
import os


class FileNotFound(Exception):
    """Exception raised when sar file isn't found"""
    pass


def parse_date(startdate_str):
    """parse the date SAR collection started"""
    formats = ['%y-%m-%d', '%Y-%m-%d', '%m/%d/%y']
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
        raise FileNotFound('file "%s" does not exist' % filename)

    def getstatsline():
        retstr = format_time(startdate, vals[0], vals[1])
        for stat in stats:
            retstr += ',%s' % vals[headermap[stat]]

        return retstr

    with open(filename, 'r') as _file:
        headerstr = ','.join(['#Time'] + stats)
        retvals.append(headerstr)

        header = _file.readline()
        header = header.split()
        startdate = parse_date(header[3])
        starttime = None

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
                headermap = {n: idx for (idx, n) in enumerate(vals)}
                continue

            if vals[0] == starttime and len(retvals) > 2:
                return retvals

            if starttime:
                if not key:
                    retvals.append(getstatsline())
                elif vals[2] == key:
                    retvals.append(getstatsline())

    return retvals
