#!/usr/bin/python

"""Simple profiler script"""

try:
    import cProfile as profile
except ImportError:
    import profile

from cStringIO import StringIO
import sys

import _bench
import intelhex


n, hexstr, ih_obj = _bench.get_100K_100K()

def read_closure():
    sio = StringIO(hexstr)
    ih = intelhex.IntelHex()
    def _run_read():
        ih.loadhex(sio)
    return _run_read

run_read = read_closure()

def write_closure():
    sio = StringIO()
    def _run_write():
        ih_obj.writefile(sio)
    return _run_write

run_write = write_closure()


if __name__ == '__main__':
    print 'Profile 100K+100K data pattern'
    print
    print 'Read operation:'
    profile.run('run_read()')
    print 'Write operation:'
    profile.run('run_write()')
