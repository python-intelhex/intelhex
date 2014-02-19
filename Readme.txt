==========================================
Intel HEX file format reader and convertor
==========================================
---------------------
Python implementation
---------------------

Author: Alexander Belchenko
Contact: alexander dot belchenko at gmail dot com
Date: 2014/mm/dd
Version: 2.0

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
Intelhex library supports Python 2 (2.4-2.7) and Python 3 (3.3) without
external libraries or 2to3 tool. Enjoy.
