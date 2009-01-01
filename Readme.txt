==========================================
Intel HEX file format reader and convertor
==========================================
---------------------
Python implementation
---------------------

Author: Alexander Belchenko
Contact: bialix AT ukr net
Date: 2009-01-01
Version: 1.0

Introduction
------------
The Intel HEX file format widely used in microprocessors and microcontrollers
area as the de-facto standard for representation of code for programming
microelectronic devices.

This work implements a HEX (also known as Intel HEX) file format reader
and convertor to binary form as a python script.

Python package **intelhex** contains implementation of a HEX file reader 
and convertor as the IntelHex class.  Also included are some scripts to do
basic tasks that utilize this package.  The ``bin2hex.py`` script converts
binary data to HEX, and the ``hex2bin.py`` works the other direction.
``hex2dump.py`` converts data from HEX to a hexdump, and ``hexmerge.py``
merges multiple HEX files into one.

License
-------
The code distributed under BSD license. See LICENSE.txt in sources archive.

Download
--------
http://www.bialix.com/intelhex/intelhex-1.0.zip

Install
-------
python setup.py install

Project at Launchpad
--------------------
Intelhex project at Launchpad.net:

    https://launchpad.net/intelhex/

There is bug tracker and source code history browser. I use Bazaar version
control system for development of intelhex.
    
Bzr (Bazaar version-control system) itself is here: 
http://bazaar-vcs.org

Documentation
-------------
User manual for IntelHex available in the sources docs/manual/ directory.
You can browse User Manual online:
http://www.bialix.com/intelhex/manual/

You can use epydoc for creating API documentation for IntelHex class. Run:

    $ python epydoc.py intelhex

You can browse API documentation online:
http://www.bialix.com/intelhex/api/

epydoc tool: http://epydoc.sourceforge.net/
