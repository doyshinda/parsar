# ParSAR

ParSAR is a Python SAR parser designed to quickly and easily parse SAR data from plain-text SAR files.

It can be run from either the command line:

    $ time ./parsar.py cpu sample.txt > /tmp/parsar.out
    real    0m0.579s
    user    0m0.552s
    sys 0m0.008s

    $ wc -l /tmp/parsar.out
    7726 /tmp/parsar.out

Or in Python code:

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
    Getting 7726 cpu stats took 0.57 seconds.

And produces output that is easy for graphing tools to consume:

    $ head -n 10 /tmp/parsar.out
    #Time,%idle
    2017-05-08T14:58:41,84.670000
    2017-05-08T14:58:44,96.270000
    2017-05-08T14:58:47,73.070000
    2017-05-08T14:58:50,73.170000
    2017-05-08T14:58:53,60.560000
    2017-05-08T14:58:56,74.410000
    2017-05-08T14:58:59,67.880000
    2017-05-08T14:59:02,41.300000
    2017-05-08T14:59:05,62.890000
