==========================================
Intel HEX file format reader and convertor
==========================================
---------------------
Python implementation
---------------------

:Author: Alexander Belchenko
:Contact: bialix@ukr.net
:Date: 2005-06-26
:Version: 0.5


Introduction
============
Intel HEX file format widely used in microprocessors and microcontrollers
area as de-facto standard for representation of code for programming into
microelectronic devices.

This work implements HEX file format reader and convertor to binary form 
as python script.

Script intelhex.py
==================
Script intelhex.py contain implementation of HEX file reader and convertor
as IntelHex class. You also may use this script as standalone hex-to-bin
convertor.

IntelHex class
--------------
Example of typical usage of IntelHex class::

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

Documentation
-------------
You can use epydoc_ for creating documentation for IntelHex class. Run epydoc::

	$ python epydoc.py intelhex

.. _epydoc: http://epydoc.sourceforge.net/


Hex-to-Bin convertor
--------------------
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
