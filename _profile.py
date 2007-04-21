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

def run_read():
    sio = StringIO(hexstr)
    ih = intelhex.IntelHex(sio)
    sio.close()

def run_write():
    sio = StringIO()
    ih_obj.writefile(sio)
    sio.close()

if __name__ == '__main__':
    print 'Profile 100K+100K data pattern'
    print
    print 'Read operation:'
    profile.run('run_read()')
    print 'Write operation:'
    profile.run('run_write()')
