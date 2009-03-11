#!/usr/bin/python
# (c) Alexander Belchenko, 2007

"""Benchmarking.

Run each test 3 times and get median value.
Using 10K array as base test time.

Each other test compared with base with next formula::

         Tc * Nb
    q = ---------
         Tb * Nc

Here:

* Tc - execution time of current test
* Tb - execution time of base
* Nb - array size of base (10K)
* Nc - array size of current test

If resulting value is ``q <= 1.0`` it's the best possible result,
i.e. time increase proportionally to array size.
"""

from cStringIO import StringIO
import gc
import sys
import time

import intelhex


def median(values):
    """Return median value for the list of values.
    @param  values:     list of values for processing.
    @return:            median value.
    """
    values.sort()
    n = int(len(values) / 2)
    return values[n]

def run_test(func, fobj):
    """Run func with argument fobj and measure execution time.
    @param  func:   function for test
    @param  fobj:   data for test
    @return:        execution time
    """
    gc.disable()
    try:
        begin = time.time()
        func(fobj)
        end = time.time()
    finally:
        gc.enable()
    return end - begin

def run_readtest_N_times(func, hexstr, n):
    """Run each test N times.
    @param  func:   function for test
    @param  hexstr: string with content of hex file to read
    @param  n:      times to repeat.
    @return:        (median time, times list)
    """
    assert n > 0
    times = []
    for i in xrange(n):
        sio = StringIO(hexstr)
        times.append(run_test(func, sio))
        sio.close()
    t = median(times)
    return t, times

def run_writetest_N_times(func, n):
    """Run each test N times.
    @param  func:   function for test
    @param  n:      times to repeat.
    @return:        (median time, times list)
    """
    assert n > 0
    times = []
    for i in xrange(n):
        sio = StringIO()
        times.append(run_test(func, sio))
        sio.close()
    t = median(times)
    return t, times

def time_coef(tc, nc, tb, nb):
    """Return time coefficient relative to base numbers.
    @param  tc:     current test time
    @param  nc:     current test data size
    @param  tb:     base test time
    @param  nb:     base test data size
    @reutrn:        time coef.
    """
    tc = float(tc)
    nc = float(nc)
    tb = float(tb)
    nb = float(nb)
    q = (tc * nb) / (tb * nc)
    return q

def get_test_data(n1, offset, n2):
    """Create test data on given pattern.
    @param  n1:     size of first part of array at base address 0.
    @param  offset: offset for second part of array.
    @param  n2:     size of second part of array at given offset.
    @return:        (overall size, hex file, IntelHex object)
    """
    # make IntelHex object
    ih = intelhex.IntelHex()
    addr = 0
    for i in xrange(n1):
        ih[addr] = addr % 256
        addr += 1
    addr += offset
    for i in xrange(n2):
        ih[addr] = addr % 256
        addr += 1
    # make hex file
    sio = StringIO()
    ih.write_hex_file(sio)
    hexstr = sio.getvalue()
    sio.close()
    #
    return n1+n2, hexstr, ih

def get_base_10K():
    """Base 10K"""
    return get_test_data(10000, 0, 0)

def get_100K():
    return get_test_data(100000, 0, 0)

def get_100K_100K():
    return get_test_data(100000, 1000000, 100000)

def get_0_100K():
    return get_test_data(0, 1000000, 100000)

def get_1M():
    return get_test_data(1000000, 0, 0)


def measure(data, n):
    """Do measuring of read and write operations.
    @param  data:   3-tuple from get_test_data
    @param  n:      repeat n times
    @return:        (time readhex, time writehex)
    """
    _, hexstr, ih = data
    tread = run_readtest_N_times(intelhex.IntelHex, hexstr, n)[0]
    twrite = run_writetest_N_times(ih.write_hex_file, n)[0]
    return tread, twrite

def print_report(results):
    base_title, base_times, base_n = results[0]
    base_read, base_write = base_times
    read_report = ['%-10s\t%7.3f' % (base_title, base_read)]
    write_report = ['%-10s\t%7.3f' % (base_title, base_write)]

    for item in results[1:]:
        cur_title, cur_times, cur_n = item
        cur_read, cur_write = cur_times
        qread = time_coef(cur_read, cur_n,
                          base_read, base_n)
        qwrite = time_coef(cur_write, cur_n,
                           base_write, base_n)
        read_report.append('%-10s\t%7.3f\t%7.3f' % (cur_title,
                                                   cur_read,
                                                   qread))
        write_report.append('%-10s\t%7.3f\t%7.3f' % (cur_title,
                                                    cur_write,
                                                    qwrite))

    print 'Read operation:'
    print '\n'.join(read_report)
    print
    print 'Write operation:'
    print '\n'.join(write_report)
    print

def main(argv=None):
    """Main function to run benchmarks.
    @param  argv:   command-line arguments.
    @return:        exit code (0 is OK).
    """
    # number of repeat
    n = 3

    results = []

    # get base numbers
    base_10K = get_base_10K()
    base_times = measure(base_10K, n)
    results.append(('base 10K', base_times, base_10K[0]))

    # 100K
    data_100K = get_100K()
    time_100K = measure(data_100K, n)
    results.append(('100K', time_100K, data_100K[0]))

    # 1M
    data_1M = get_1M()
    time_1M = measure(data_1M, n)
    results.append(('1M', time_1M, data_1M[0]))

    # 100K + 100K
    data_100K_100K = get_100K_100K()
    time_100K_100K = measure(data_100K_100K, n)
    results.append(('100K+100K', time_100K_100K, data_100K_100K[0]))

    # 0 + 100K
    data_0_100K = get_0_100K()
    time_0_100K = measure(data_0_100K, n)
    results.append(('0+100K', time_0_100K, data_0_100K[0]))

    print_report(results)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
