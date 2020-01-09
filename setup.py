#!/usr/bin/python

# Copyright (c) 2008-2018, Alexander Belchenko
# All rights reserved.
#
# Redistribution and use in source and binary forms,
# with or without modification, are permitted provided
# that the following conditions are met:
#
# * Redistributions of source code must retain
#   the above copyright notice, this list of conditions
#   and the following disclaimer.
# * Redistributions in binary form must reproduce
#   the above copyright notice, this list of conditions
#   and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# * Neither the name of the author nor the names
#   of its contributors may be used to endorse
#   or promote products derived from this software
#   without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING,
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY,
# OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
# PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA,
# OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED
# AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""Setup script for IntelHex."""

import sys, glob
from distutils.core import Command
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

import intelhex, intelhex.__version__

LONG_DESCRIPTION = open('Readme.rst', 'r').read()

METADATA = dict(
      name='intelhex',
      version=intelhex.__version__.version_str,

      scripts=glob.glob('scripts/*'),
      packages=['intelhex'],

      author='Alexander Belchenko',
      author_email='alexander.belchenko@gmail.com',
      maintainer='Bert van Hall',
      maintainer_email='bert.vanhall@gmx.de',
      url='https://github.com/python-intelhex/intelhex',
      description='Python library for Intel HEX files manipulations',
      long_description=LONG_DESCRIPTION,
      keywords='Intel HEX hex2bin HEX8',
      license='BSD',
      classifiers = [
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
      ],
)


class test(Command):
    description = "unittest for intelhex"
    user_options = []
    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import unittest
        import intelhex.test
        verbosity = 1
        if self.verbose:
            verbosity = 2
        suite = unittest.TestSuite()
        loader = unittest.TestLoader()
        suite.addTest(loader.loadTestsFromModule(intelhex.test))
        runner = unittest.TextTestRunner(stream=sys.stdout, verbosity=verbosity)
        result = runner.run(suite)
        if result.errors or result.failures:
            sys.exit(1)


class bench(Command):
    description = "benchmarks for read/write HEX"
    user_options = [
        ('repeat', 'n', 'repeat tests N times'),
        ('read', 'r', 'run only tests for read operation'),
        ('write', 'w', 'run only tests for write operation'),
        ]
    boolean_options = ['read', 'write']

    def initialize_options(self):
        self.repeat = 3
        self.read = None
        self.write = None

    def finalize_options(self):
        if not self.read and not self.write:
            self.read = self.write = True

    def run(self):
        from intelhex.bench import Measure
        m = Measure(self.repeat, self.read, self.write)
        m.measure_all()
        m.print_report()


def main():
    metadata = METADATA.copy()
    metadata['cmdclass'] = {
        'test': test,
        'bench': bench,    # bench is out of date
        }
    return setup(**metadata)

if __name__ == '__main__':
    main()
