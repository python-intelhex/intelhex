#!/usr/bin/python

# Copyright (c) 2014-2018 Alexander Belchenko
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

""" Ad-hoc test runner against multiple python versions. """

import subprocess
import sys
import time


# TODO: extract this as some sort of config file
if sys.platform == 'win32':
    # Get from Windows registry
    # HKEY_LOCAL_MACHINE\SOFTWARE\Python
    #                                PythonCore
    #                                       2.6
    #                                           InstallPath
    #                                       2.7
    #                                       3.3
    #                                       3.4
    # HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Python\PythonCore\3.3\InstallPath
    PYTHONS = (
        # display name, executable [full] path
        #('2.3', 'C:\Python23\python'),     # 2.3 is not supported
        ('2.4', r'C:\Python\2.4\python'),
        ('2.5', r'C:\Python\2.5\python'),

        ('2.6-32bit', r'C:\Python\2.6-32\python'),
        ('2.6-64bit', r'C:\Python\2.6-64\python'),

        ('2.7-32bit', r'C:\Python\2.7-32\python'),
        ('2.7-64bit', r'C:\Python\2.7-64\python'),

        ('3.2-32bit', r'C:\Python\3.2-32\python'),
        ('3.2-64bit', r'C:\Python\3.2-64\python'),

        ('3.3-32bit', r'C:\Python\3.3-32\python'),
        ('3.3-64bit', r'C:\Python\3.3-64\python'),

        ('3.4-32bit', r'C:\Python\3.4-32\python'),
        ('3.4-64bit', r'C:\Python\3.4-64\python'),

        ('3.5-32bit', r'C:\Python\3.5-32\python'),
        ('3.5-64bit', r'C:\Python\3.5-64\python'),

        ('pypy',      r'C:\Python\pypy-2.5.1-win32\pypy'),
        )
else:
    PYTHONS = (
        # display name, executable [full] path
        ('2.4', 'python2.4'),
        ('2.5', 'python2.5'),
        ('2.6', 'python2.6'),
        ('2.7', 'python2.7'),
        ('3.3-32bit', 'python3.3-32'),
        ('3.3-64bit', 'python3.3-64'),
        )


def main():
    retcode = 0
    not_found = []
    failed = []
    print('%s started: %s\n' % (__file__, time.asctime()))
    for display_name, executable in PYTHONS:
        if checkPythonExists(display_name, executable):
            if not runTestWithPython(display_name, executable):
                retcode = 1
                failed.append(display_name)
        else:
            not_found.append(display_name)
    if failed or not_found:
        print('\n' + '-'*20)        
    if failed:
        print('Tests failed with pythons: %s' % (', '.join(failed)))
    if not_found:
        print('Not found python versions: %s' % (', '.join(not_found)))
    return retcode

def checkPythonExists(display_name, executable):
    """ Run `python -V` and check that it runs OK. """
    sys.stdout.write('Check presence of python %s ... ' % display_name)
    cmd = '%s -V' % executable
    try:
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    except:
        exc = sys.exc_info()[1]     # current exception
        sys.stdout.write('ERROR\n  Exception: %s\n' % str(exc))
        return False
    stdout, stderr = p.communicate()
    retcode = p.poll()
    output = ''
    if stdout:
        output = stdout.decode('ascii', 'replace')
    elif stderr:
        output = stderr.decode('ascii', 'replace')        
    output = output.replace('\r', '')
    if not output.endswith('\n'):
        output = output + '\n'
    output = output.replace(u'\ufffd', u'?')
    sys.stdout.write(output)
    return retcode == 0

def runTestWithPython(display_name, executable):
    """ Runs `$(PYTHON) setup.py test -q` """
    cmd = '%s setup.py test -q' % executable
    sys.stdout.write('   Running tests against %s ... ' % display_name)
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    stdout, stderr = p.communicate()
    retcode = p.poll()
    if retcode == 0:
        sys.stdout.write('OK\n')
        return True
    else:
        sys.stdout.write('FAILED\n')
        sys.stdout.write(stdout.decode('ascii', 'ignore'))
        sys.stdout.write(stderr.decode('ascii', 'ignore'))
        return False

if __name__ == '__main__':
    sys.exit(main())
