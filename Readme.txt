-----------------------
Python IntelHex library
-----------------------

Author: Alexander Belchenko
Contact: alexander belchenko at gmail com
Date: 2015/04/12
Version: 2.0

Introduction
------------
The Intel HEX file format is widely used in microprocessors and microcontrollers 
area as the de facto standard for code representation for microelectronic devices programming.

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
The code is distributed under BSD license. See LICENSE.txt in the sources archive.

In short: you can use IntelHex library in your project without any restrictions.

If you're using IntelHex library in your open-source project, or your company 
created freely available set of tools, utilities or sdk based on IntelHex
library, please send me an email and tell something about your project. 
I'd like to add the name of your project/company to page "Who Uses IntelHex".

Python 3 compatibility
----------------------
Intelhex library supports Python 2 (2.4-2.7) and Python 3 (3.3 and later) 
without external libraries or 2to3 tool from the same codebase.

Download
--------
* https://pypi.python.org/pypi/IntelHex
* https://launchpad.net/intelhex/+download
* https://github.com/bialix/intelhex

Install
-------
Install using pip (no separate download required):

    pip install intelhex

Install from sources (classic python's magic spell):

    python setup.py install

Source code
-----------
Intelhex project on Launchpad:

    https://launchpad.net/intelhex/
    
Get code with bzr:
    
    bzr branch lp:intelhex

IntelHex on GitHub:

    https://github.com/bialix/intelhex
    
Get code with git:

    git clone https://github.com/bialix/intelhex.git

User manual
-----------
User manual for IntelHex is available in the sources docs/manual/ directory.
You can browse User Manual online:

    http://pythonhosted.org/IntelHex/

API documentation
-----------------
You can use epydoc for creating API documentation for IntelHex class. Run:

    $ python epydoc.py intelhex

epydoc tool: http://epydoc.sourceforge.net/
