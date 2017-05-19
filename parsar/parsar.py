import argparse
from . import cparsar


DEFAULT_CPU_STATS = ['%idle']
DEFAULT_MEM_STATS = ['%memused']
DEFAULT_DISK_STATS = ['tps']


# Section identifiers
CPU = 'CPU|%usr'
MEM = 'kbmemfree|kbmemused'
DISK = 'DEV|tps'


class FileNotFound(Exception):
    """Exception raised when sar file isn't found"""
    pass


class IncompatibleFileType(Exception):
    """Exception raised when parsar can't parse the file (most likely means
    the user passed in the binary sa file)"""
    pass


class ParsarException(Exception):
    """General catch all exception"""
    pass


def _try_parse(filename, section, stats, **kwargs):
    """Attempt to parse the <filename>, raising appropriate
    exception if it fails."""
    try:
        resp = cparsar.parsefile(filename, section, stats, **kwargs)

        if isinstance(resp, list):
            return resp

        if resp == cparsar.ENOENT:
            raise FileNotFound('file "%s" does not exist' % filename)
        elif resp == cparsar.EMEDIUMTYPE:
            msg = 'incompatible file detected, parsar requires SAR text ' \
                  'files, perhaps "%s" is the binary version?'
            raise IncompatibleFileType(msg % filename)
        else:
            raise ParsarException('Unexpected err code returned: "%s"' % resp)

    except Exception as e:  # pylint: disable=W0703
        raise ParsarException(e)


class Parsar(object):
    """Parsar class"""

    def __init__(self, filename):
        self.filename = filename

    # pylint: disable=E1101
    def cpu(self, stats=DEFAULT_CPU_STATS):
        return _try_parse(self.filename, CPU, stats, key='all')

    def mem(self, stats=DEFAULT_MEM_STATS):
        return _try_parse(self.filename, MEM, stats)

    def disk(self, devname, stats=DEFAULT_DISK_STATS):
        return _try_parse(self.filename, DISK, stats, key=devname)


def get_args():
    """get command line arguments"""
    parser = argparse.ArgumentParser(description='Parse SAR data')
    subparsers = parser.add_subparsers(help='SAR Section of interest')

    subparser = subparsers.add_parser('cpu', help='CPU stats')
    subparser.add_argument('--cpustats', nargs='*')

    subparser = subparsers.add_parser('mem', help='Memory stats')
    subparser.add_argument('--memstats', nargs='*')

    subparser = subparsers.add_parser('disk', help='Disk stats')
    subparser.add_argument('--diskdev', required=True,
                           help='desired disk device')
    subparser.add_argument('--diskstats', nargs='+',
                           help='default: %s' % DEFAULT_DISK_STATS[0])

    parser.add_argument('filename', help='the SAR file to parse')
    return parser.parse_args()


def main():
    """main entry point"""
    args = get_args()
    p = Parsar(args.filename)
    if hasattr(args, 'cpustats'):
        stats = args.cpustats or DEFAULT_CPU_STATS
        result = p.cpu(stats=stats)
    elif hasattr(args, 'memstats'):
        stats = args.memstats or DEFAULT_MEM_STATS
        result = p.mem(stats=stats)
    elif hasattr(args, 'diskstats'):
        stats = args.diskstats or DEFAULT_DISK_STATS
        result = p.disk(args.diskdev, stats=stats)

    # TODO: Handle broken pipe (i.e., piping output into head)
    for r in result:
        print(r)