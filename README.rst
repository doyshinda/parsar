Parsar
======

Parsar is a Python SAR parser designed to quickly and easily parse SAR data from plain-text SAR files.
 
It can be run from either the command line::

    $ time parsar cpu sample.txt > /tmp/parsar.out
    real    0m0.277s
    user    0m0.268s
    sys     0m0.004s

    $ wc -l /tmp/parsar.out
    7794 /tmp/parsar.out
 
Or in Python code::

    >>> import parsar
    >>> import time
    >>> p = parsar.Parsar('sample.txt')
    >>> def getcpustats():
    ...     start = time.time()
    ...     data = p.cpu()
    ...     end = time.time()
    ...     print 'Getting %d cpu stats took %.2f seconds.' % (len(data), (end - start))
    ...
    >>> getcpustats()
    Getting 7794 cpu stats took 0.23 seconds.

And produces CSV output that is easy for graphing tools to consume::

    $ head -n 10 /tmp/parsar.out
    #Time,%idle
    2017-05-08T21:11:09,79.92
    2017-05-08T21:11:12,89.86
    2017-05-08T21:11:15,77.42
    2017-05-08T21:11:18,63.74
    2017-05-08T21:11:21,69.48
    2017-05-08T21:11:24,44.79
    2017-05-08T21:11:27,55.61
    2017-05-08T21:11:30,60.89
    2017-05-08T21:11:33,74.08

Supports returning whatever data column(s) you're interested in::

    $ parsar cpu --cpustats %usr %iowait sample.txt > /tmp/parsar.out
    $ head -n 10 /tmp/parsar.out
    #Time,%usr,%iowait
    2017-05-08T21:11:09,3.95,13.25
    2017-05-08T21:11:12,3.90,5.41
    2017-05-08T21:11:15,6.93,13.02
    2017-05-08T21:11:18,4.87,26.74
    2017-05-08T21:11:21,9.15,19.98
    2017-05-08T21:11:24,17.04,34.81
    2017-05-08T21:11:27,23.35,16.41
    2017-05-08T21:11:30,3.48,32.10
    2017-05-08T21:11:33,6.13,18.62
