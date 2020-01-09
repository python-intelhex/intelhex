*****************
IntelHex releases
*****************

2.2.1 (2018-01-30)
------------------
* Fixes for PyPI.

2.2 (2018-01-28)
----------------
* API changes: ``IntelHex.write_hex_file`` method: added support for new
  parameter: ``eolstyle = native | CRLF``. (Alexander Belchenko)
* API changes: ``IntelHex.write_hex_file()`` method gets new optional 
  parameter ``byte_count`` to specify how many bytes should be written
  to each data record in output file. Default value is 16.
  (patch from GitHub user erki1993)
* Unit tests: Fixed xrange overflow test for Python 2.7 on 64-bit platforms.
  Use ``sys.maxint`` to ensure we trigger an exception. (Masayuki Takeda)
* Script ``hexinfo.py``: Python 3 compatibility for processing start address
  dict keys. (patch from GitHub user mentaal)
* Added ``get_memory_size()`` method: approx memory footprint of IntelHex object
  plus data. (Alexander Belchenko)
* Better compatibility with Python 3. (Alexander Belchenko)

2.1 (2016-03-31)
----------------
* API changes: added ``IntelHex.segments()`` method that returns
  a list of ordered tuple objects, representing contiguous occupied data 
  addresses. (Andrew Fernandes)
* New command-line script ``hexinfo.py`` to print summary about hex files
  contents (file name, start address, address ranges covered by the data)
  in YAML format. (Andrew Fernandes)
* Better Python 3 compatibility when ``hex2bin.py`` and ``bin2hex.py``
  scripts are trying to read/write binary data from stdin or to stdout.
  (GitHub issue https://github.com/python-intelhex/intelhex/issues/4)
* The main activity of the IntelHex project slowly drifting towards
  GitHub - the main social network for OSS developers.
  I'd really like to get some help from additional maintainer though.
* API changes: ``IntelHex.dump()`` method gets new optional parameters:
  ``width``, ``withpadding`` to control generation of output text.
  (patch from GitHub user durexyl)
* Script ``hex2dump.py`` gets new option ``--width`` to support
  corresponding parameter in ``IntelHex.dump()`` method.

2.0 (2015-04-12)
----------------
* The same codebase can be run on both Python 2 (2.4-2.7) 
  and Python 3 (3.2+). No need to use 2to3.
* ``compat.py``: provide more helper functions and aliases to reduce changes
  required to convert python 2 compatible sources to python 3. 
  The code becomes quite ugly, but such compatibility has its price.
* Python 3 compatibility: tobinstr should return bytes not unicode string
  (Bug #1212698).
* Python 2: better support for long int addresses (over 2GB)
  (Bug #1408934)

1.5 (2013-08-02)
----------------
* API changes: Functions tobinarray/tobinstr/tobinfile:
  pad parameter is deprecated and will be removed in
  future releases. Use IntelHex.padding attribute instead,
  and don't pass pad as None explicitly please.
  If you need to use size parameter, then use syntax like that:
  ``ih.tobinarray(start=xxx, size=yyy)``
* API changes: Functions tobinarray/tobinstr/tobinfile:
  default value of pad is None now (was ``0xFF``) 
  to allow using value of ``IntelHex.padding``
  if no explicit pad specified.
* Fixed bug: wrong ``getopt`` error handling in some scripts.
  (Thanks to Andy Mozhevilov for bug report)
* PEP-8 style improvements. (Thanks to Stefan Schmitt)
* ``IntelHex16bit.tobinarray`` method returns array of unsigned short
  (words) values. (Feature request from Stefan Schmitt)
* Improved Python 3 compatibility (don't use old file() function).
  (Thanks to Luis Panadero Guardeño for bug report)

1.4 (2012-04-25)
----------------
* New feature: compare 2 hex files using hex dump
  as string representation. Feature available as
  worker function diff_dumps() and as command-line
  utility hexdiff.py (#627924).
* Changes in the codebase suggested by 2to3 tool to provide
  compatibility with Python3. Now sources can be successfully
  converted to Python3 with 2to3 utility. 
  See Python 3 notes in README.txt and documentation.
  (Thanks to Bernhard Leiner for his help)
* Fixed bug #988148: ``IntelHex16bit`` should copy all public attributes
  from source IntelHex 8-bit object. (Thanks to Morgan McClure)

1.3 (2010-11-24)
----------------
* ``hex2dump``: show 0x7F character as dot for better compatibility 
  with GNU less utility.
* tobinarray, tobinfile, tobinstr: added size parameter. (Bug #408748)
* fixed error in ``hexmerge.py`` script. (#676023)

1.2 (2009-08-04)
----------------
* Fixed bug 372620: tobinarray on empty file should return pad bytes 
  when address range explicitly specified.
* Improved docstrings: explicitly say that ``end`` param of to-* methods 
  is always inclusive. (see bug #372625 for details).
* Improved documentation on ``ih.dump(tofile)``.

1.1 (2009-03-12)
----------------
* Fixed bug in writing hex files with small chains of bytes
* Improved Python 2.6 compatibility

1.0 (2009-01-01)
----------------
* Improved API, better performance
* New User Manual (Zachary Clifford)

0.9 (2007-06-16)
----------------
New API release.

* New API
* Performance improvements: read hex file now ~45% faster

0.8.6 (2007-04-27)
------------------
Bug fixes and performance improvements.

* ``IntelHex`` is able to read/write start address records
  (HEX record type ``03`` and ``05``). (fix bug #109872)
* Backport (from 0.9 branch) of performance improvements 
  for reading hex files

0.8.5 (2007-02-26)
------------------
BugFix Release.

Performance improvements for writing big hex files
when starting address is far from 0. Patch from Heiko Henkelmann.
       
0.8.4 (2007-02-26)
------------------
License added.

The code is actually licensed under BSD, but there was 
no LICENSE file in sources archive. Added license file
and explicit declaration in the source code.

0.8.3 (2006-09-05)
------------------
BugFix Release.

Fix writing hex files with extended linear records
(when address overlaps 64K boundary). Patch from Henrik Maier.
    
0.8.2 (2006-04-11)
------------------
Major improvements release.

* Introduced new class ``IntelHex16bit`` for manipulate data as 16-bit values
* You can manipulate data using dictionary-like interface
  (i.e. syntax like: ``ih[addr] = value``)
* Added new method ``writefile(file)`` for writing data to hex file
* Using unittest for testing functionality
    
0.6 (2006-03)
-------------
Convertor engine ``hex2bin`` extracted to stand-alone function
for using by external clients of intelhex.
    
0.5 (2005)
----------
First public release.
