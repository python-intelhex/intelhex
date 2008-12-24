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
merges multiple HEX files into one

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

In the second line we are creating an instance of the class. The constructor
optionally takes the name of the HEX file or a file-like object. If specified,
the file is automatically read and decoded.

In version 0.9 the API slightly changed. Now you can create an empty object
and load data later.  You can also load data several times (but if addresses
in those files overlap you get exception ``AddressOverlapError``). This error
is only raised when reading from hex files. When reading from other formats,
without explicitly calling ``merge``, the data will be overwritten. E.g.::

	>>> from intelhex import IntelHex
	>>> ih = IntelHex()			# create empty object
	>>> ih.loadhex('foo.hex')		# load from hex
	>>> ih.loadfile('bar.hex',format='hex')	# also load from hex
	>>> ih.fromfile('bar.hex',format='hex')	# also load from hex

NOTE: using IntelHex.fromfile is recommended way.

Access to data by address
*************************
You can get or modify some data by address in the usual way: via indexing
operations::

	>>> print ih[0]			# read data from address 0
	>>> ih[1] = 0x55		# modify data at address 1

When you try to read from non-existent address you get default data. Default
data is set via attribute ``.padding`` of class instance.

To obtain adress limits use methods ``.minaddr()`` and ``.maxaddr()``.

Access to 16-bit data
*********************
When you need to work with 16-bit data stored in 8-bit Intel HEX files you need
to use class ``IntelHex16bit``. This class is derived from IntelHex and has all 
its methods. Some of methods have been modified to implement 16-bit behaviour.
This class assumes the data is in Little Endian byte order.

Convert data to binary form
***************************
Class IntelHex has 3 methods for converting data of IntelHex objects
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

NOTE: using IntelHex.tofile is the recommended way.

Write data to HEX file
**********************
You can store data contained in object by method ``.write_hex_file(f)``.
Parameter ``f`` should be filename or file-like object. Also you can use the
universal tofile.

To convert data of IntelHex object to HEX8 file format without actually saving
it to disk you can use the builtin StringIO file-like object, e.g.::

	>>> from cStringIO import StringIO
	>>> from intelhex import IntelHex
	>>> ih = IntelHex()
	>>> ih[0] = 0x55

	>>> sio = StringIO()
	>>> ih.write_hex_file(sio)
	>>> hexstr = sio.getvalue()
	>>> sio.close()

Variable ``hexstr`` will contain a string with the content of a HEX8 file.

To write data as a hex file you also can use universal method ``tofile``::

	>>> ih.tofile(sio, format='hex')

NOTE: using IntelHex.tofile is recommended way.


Start address
*************
Some linkers write to produced HEX file information about start address
(either record 03 or 05). Now IntelHex is able correctly read such records
and store information internally in ``start_addr`` attribute that itself
is either ``None`` or a dictionary with the address value(s). 

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

When ``start_addr`` is ``None`` or an empty dictionary nothing will be written
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
You can use hex-to-bin convertor in two ways: as function ``hex2bin`` (useful
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


Bin-to-Hex convertor
--------------------
You can use bin-to-hex convertor in two ways: as function ``bin2hex`` (useful
for using in other scripts) or as stand-alone script.

Function ``bin2hex``
********************
Bin-to-Hex convertor engine.

``bin2hex(fin, fout, offset=0)``

**Parameters**: 

* ``fin`` -- input bin file (filename or file-like object) 
* ``fout`` -- output hex file (filename or file-like object) 
* ``offset`` -- starting address offset for loading bin (default: 0)

**Returns**: 

	0 if all OK 


Stand-alone script ``bin2hex.py``
**********************************
You can use bin2hex.py as simple bin-to-hex convertor. This script is 
just frontend for `Function bin2hex`_ described above.
::

    Usage:
        python bin2hex.py [options] INFILE [OUTFILE]
    
    Arguments:
        INFILE      name of bin file for processing.
                    Use '-' for reading from stdin.
    
        OUTFILE     name of output file. If omitted then output
                    will be writing to stdout.
    
    Options:
        -h, --help              this help message.
        --offset=N              offset for loading bin file (default: 0).

Stand-alone script ``hex2dump.py``
***********************************
This is a script to dump a hex file to a hexdump format. It is a frontend for
dump in IntelHex.
::

    Usage:
        python hex2dump.py [options] HEXFILE

    Options:
        -h, --help              this help message.
        -r, --range=START:END   specify address range for dumping
                                (ascii hex value).
                                Range can be in form 'START:' or ':END'.

    Arguments:
        HEXFILE     name of hex file for processing (use '-' to read
                    from stdin)

Stand-alone script ``hexmerge.py``
***********************************
This is a script to merge two different hex files. It is a frontend for the
merge function in IntelHex.
::

    Usage:
        python hexmerge.py [options] FILES...

    Options:
        -h, --help              this help message.
        -o, --output=FILENAME   output file name (emit output to stdout
                                if option is not specified)
        -r, --range=START:END   specify address range for output
                                (ascii hex value).
                                Range can be in form 'START:' or ':END'.
        --no-start-addr         Don't write start addr to output file.
        --overlap=METHOD        What to do when data in files overlapped.
                                Supported variants:
                                * error -- stop and show error message (default)
                                * ignore -- keep data from first file that
                                            contains data at overlapped address
                                * replace -- use data from last file that
                                             contains data at overlapped address

    Arguments:
        FILES       list of hex files for merging
                    (use '-' to read content from stdin)

    You can specify address range for each file in the form:

        filename:START:END

    See description of range option above.

    You can omit START or END, so supported variants are:

        filename:START:     read filename and use data starting from START addr
        filename::END       read filename and use data till END addr

    Use entire file content:

        filename
    or
        filename::

