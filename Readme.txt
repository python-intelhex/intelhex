==========================================
Intel HEX file format reader and convertor
==========================================
---------------------
Python implementation
---------------------

Author: Alexander Belchenko
Contact: alexander dot belchenko at gmail dot com
Date: yyyy/mm/dd
Version: 1.5.1

Introduction
------------
The Intel HEX file format widely used in microprocessors and microcontrollers 
area as the de-facto standard for representation of code for programming 
microelectronic devices.

This work implements an **intelhex** Python library to read, write, 
create from scratch and manipulate data from HEX (also known as Intel HEX) 
file format. These operations are provided by ``IntelHex`` class.

The distribution package also includes several convenience Python scripts
to do basic tasks that utilize this library. The ``bin2hex.py`` script 
converts binary data to HEX, and the ``hex2bin.py`` works the other direction. 
``hex2dump.py`` converts data from HEX to a hexdump which is useful for
inspecting data, and ``hexmerge.py`` merges multiple HEX files into one.

License
-------
The code distributed under BSD license. See LICENSE.txt in sources archive.

Download
--------
https://launchpad.net/intelhex/+download

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
http://bazaar.canonical.com

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

Python 3 compatibility
----------------------
Intelhex library developed using Python 2 and supposed to support
Python 2.4 and higher.

In addition there was added support for Python 3. To use Intelhex library on
Python 3 you should translate its sources with 2to3 utility.

You can make such translation manually with help of Makefile in sources:

    make 2to3 PYTHON=python3

Alternatively sources and scripts will be automatically translated while
executing standard install spell:

    python3 setup.py build install
