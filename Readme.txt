==========================================
Intel HEX file format reader and convertor
==========================================
---------------------
Python implementation
---------------------

:Author: Alexander Belchenko
:Contact: bialix AT ukr net
:Date: 2008-08-19
:Version: 1.0

.. Contents::

Introduction
------------
Intel HEX file format widely used in microprocessors and microcontrollers
area as de-facto standard for representation of code for programming into
microelectronic devices.

This work implements HEX (also known as Intel HEX) file format reader
and convertor to binary form as python script.

Python package **intelhex** contains implementation of HEX file reader 
and convertor as IntelHex class. You also may use ``hex2bin.py`` script 
as handy hex-to-bin convertor.


License
-------
The code distributed under BSD license. See LICENSE.txt in sources achive.


Download
--------
XXX

.. http://www.bialix.com/intelhex/intelhex.zip


Project at Launchpad
--------------------
Intelhex project at Launchpad.net:

    https://launchpad.net/intelhex/

There is bug tracker and source code history browser. I use Bazaar version
control system for development of intelhex.
    
Bzr (Bazaar version-control system) itself is here: 
http://bazaar-vcs.org


IntelHex classes
----------------
Basic
*****
Example of typical initialization of ``IntelHex`` class::

	>>> from intelhex import IntelHex
	>>> ih = IntelHex("foo.hex")

In second line we are create instance of class. Constructor has one optional 
parameter: name of HEX file or file object. 
Specified file automatically read and decoded.

In version 0.9 API slightly changed. Now you can create empty object
and load data later, and even load data several times (but if addresses
in those files overlap you get exception ``AddressOverlapError``). E.g.::

	>>> from intelhex import IntelHex
	>>> ih = IntelHex()			# create empty object
	>>> ih.loadhex('foo.hex')		# load from hex
	>>> ih.loadfile('bar.hex',format='hex')	# also load from hex

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

Convert data to binary form
***************************
Class IntelHex has 3 methods for converting data of IntelHex object
into binary form:

	* ``tobinarray`` (returns array of unsigned char bytes);
	* ``tobinstr``   (returns string of bytes);
	* ``tobinfile``  (convert content to binary form and write to file).
        
Example::

	>>> from intelhex import IntelHex
	>>> ih = IntelHex("foo.hex")
	>>> ih.tobinfile("foo.bin")

To write data as binary file you also can use universal method ``tofile``::

	>>> ih.tofile("foo.bin", format='bin')

Write data to HEX file
**********************
You can store data contained in object by method ``.write_hex_file(f)``. Parameter
``f`` should be filename or file-like object. Also you can use universal

To convert data of IntelHex object to HEX8 file format without actually saving
it to disk you can use StringIO file-like object, e.g.::

	>>> from cStringIO import StringIO
	>>> from intelhex import IntelHex
	>>> ih = IntelHex()
	>>> ih[0] = 0x55

	>>> sio = StringIO()
	>>> ih.write_hex_file(sio)
	>>> hexstr = sio.getvalue()
	>>> sio.close()

Variable ``hexstr`` will contains string with content of HEX8 file.

To write data as hex file you also can use universal method ``tofile``::

	>>> ih.tofile(sio, format='hex')


Start address
*************
Some linkers write to produced HEX file information about start address
(either record 03 or 05). Now IntelHex is able correctly read such records
and store information internally in ``start_addr`` attribute that itself
is ``None`` or dictionary with address value(s). 

When input HEX file contains record type 03 (Start Segment Address Record),
``start_addr`` takes value::

	{'CS': XXX, 'IP': YYY}
        
Here:

	* ``XXX`` is value of CS register
	* ``YYY`` is value of IP register

To obtain or change ``CS`` or ``IP`` value you need to use their names
as keys for ``start_addr`` dictionary::

	>>> ih = IntelHex('file_with_03.hex')
	>>> print ih.start_addr['CS']
	>>> print ih.start_addr['IP']

When input HEX file contains record type 05 (Start Linear Address Record),
``start_addr`` takes value::

	{'EIP': ZZZ}

Here ``ZZZ`` is value of EIP register.

Example::

	>>> ih = IntelHex('file_with_05.hex')
	>>> print ih.start_addr['EIP']

You can manually set required start address::

	>>> ih.start_addr = {'CS': 0x1234, 'IP': 0x5678}
	>>> ih.start_addr = {'EIP': 0x12345678}

To delete start address info give value ``None`` or empty dictionary::

	>>> ih.start_addr = None
	>>> ih.start_addr = {}

When you write data to HEX file you can disable writing start address
with additional argument ``write_start_addr``:

	>>> ih.write_hex_file('out.hex')	# by default writing start address
	>>> ih.write_hex_file('out.hex', True)	# as above
	>>> ih.write_hex_file('out.hex', False)	# don't write start address

When ``start_addr`` is ``None`` or empty dictionary nothing will be written
regardless of ``write_start_addr`` argument value.


Documentation
-------------
You can use epydoc_ for creating documentation for IntelHex class. Run epydoc::

	$ python epydoc.py intelhex.py

.. _epydoc: http://epydoc.sourceforge.net/

`You can see API documentation on my site.`__

__ http://www.bialix.com/intelhex/api/


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


Stand-alone script ``hex2bin.py``
**********************************
You can use hex2bin.py as handy hex-to-bin convertor. This script is 
just frontend for `Function hex2bin`_ described above.
::

        Usage:
            python hex2bin.py [options] INFILE [OUTFILE]
        
        Arguments:
            INFILE      name of hex file for processing.
            OUTFILE     name of output file. If omitted then output
                        will be writing to stdout.


	Options:
	    -h, --help		    this help message.
	    -p, --pad=FF	    pad byte for empty spaces (hex value).
	    -r, --range=START:END   specify address range for writing output
				    (hex value).
				    Range can be in form 'START:' or ':END'.
	    -l, --length=NNNN,
	    -s, --size=NNNN	    size of output (decimal value).

Per example, converting content of foo.hex to foo.bin addresses from 0 to FF::

	$ python hex2bin.py -r 0000:00FF foo.hex

Or (equivalent)::

	$ python hex2bin.py -r 0000: -s 256 foo.hex
