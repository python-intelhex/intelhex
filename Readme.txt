==========================================
Intel HEX file format reader and convertor
==========================================
---------------------
Python implementation
---------------------

:Author: Alexander Belchenko
:Contact: bialix AT ukr net
:Date: 2006-09-05
:Version: 0.8.3

.. Contents::

Introduction
------------
Intel HEX file format widely used in microprocessors and microcontrollers
area as de-facto standard for representation of code for programming into
microelectronic devices.

This work implements 8-bit HEX (also known as Intel HEX8) file format reader
and convertor to binary form as python script.

Script intelhex.py contain implementation of HEX file reader and convertor
as IntelHex class. You also may use this script as standalone hex-to-bin
convertor.


Download
--------
http://www.onembedding.com/tools/python/code/intelhex.zip


IntelHex classes
----------------
Basic
*****
Example of typical usage of ``IntelHex`` class::

	>>> from intelhex import IntelHex	# 1
	>>> h = IntelHex("foo.hex")		# 2
	>>> h.readfile()			# 3
	>>> h.tobinfile("foo.bin")		# 4

In second line we are create instance of class. Constructor has one parameter:
name of HEX file or file object. For reading and decoding content of HEX file
we need to invoke ``readfile()`` method (see line 3 in example above). 
It returns True if file processed successful, or False if some error detected.
Class IntelHex has 3 methods for converting content of HEX file 
into binary form (see line 4 in example above):

	* ``tobinarray`` (returns array of unsigned char bytes);
	* ``tobinstr``   (returns string of bytes);
	* ``tobinfile``  (convert content to binary form and write to file).

Access to data by address
*************************
You can get or modify some data by address in usual way: via indexing
operations::

	>>> print ih[0]			# read data from address 0
        >>> ih[1] = 0x55		# modify data at address 1

When you try to read from non-existent address you get default data. Default
data sets via attribute ``.padding`` of class instance.

To obtain adresses limits use methods ``.minaddr()`` and ``.maxaddr()``.

Access to 16-bit data
*********************
When you need to work with 16-bit data stored in 8-bit Intel HEX file you need
to use class ``IntelHex16bit``. This class derived from IntelHex and has all their
methods. But some of methods modified to implement 16-bit behaviour.

Write data to HEX file
**********************
You can store data contained in object by method ``.writefile(f)``. Parameter
``f`` should be filename or file-like object. After writing file will be closed.


Documentation
-------------
You can use epydoc_ for creating documentation for IntelHex class. Run epydoc::

	$ python epydoc.py intelhex

.. _epydoc: http://epydoc.sourceforge.net/


Hex-to-Bin convertor
--------------------
You can use hex-to-bin convertor in two way: as function ``hex2bin`` (useful
for using in other scripts) or as stand-alone script.

Function ``hex2bin``
********************
Hex-to-Bin convertor engine.

``hex2bin(fin, fout, start=None, end=None, size=None, pad=255)``

**Parameters**: 

* ``fin`` -- input hex file (filename or file-like object) 
* ``fout`` -- output bin file (filename or file-like object) 
* ``start`` -- start of address range (optional) 
* ``end`` -- end of address range (optional) 
* ``size`` -- size of resulting file (in bytes) (optional) 
* ``pad`` -- padding byte (optional) 

**Returns**: 

	0 if all OK 


Stand-alone script ``intelhex.py``
**********************************
You can use intelhex.py as stand-alone hex-to-bin convertor.
::

	Usage:
	    python intelhex.py [options] file.hex [out.bin]

	Arguments:
	    file.hex                name of hex file to processing.
	    out.bin                 name of output file.
				    If omitted then output write to file.bin.

	Options:
	    -h, --help              this help message.
	    -p, --pad=FF            pad byte for empty spaces (hex value).
	    -r, --range=START:END   specify address range for writing output
				    (hex value).
				    Range can be in form 'START:' or ':END'.
	    -l, --length=NNNN,
	    -s, --size=NNNN         size of output (decimal value).

Per example, converting content of foo.hex to foo.bin addresses from 0 to FF::

	$ python intelhex.py -r 0000:00FF foo.hex

Or (equivalent)::

	$ python intelhex.py -r 0000: -s 256 foo.hex
