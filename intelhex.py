#!/usr/bin/python

# Copyright (c) 2005-2007, Alexander Belchenko
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
# * Neither the name of the <Alexander Belchenko>
#   nor the names of its contributors may be used to endorse
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

'''Intel HEX file format reader and converter.

This script also may be used as hex2bin convertor utility.

@author     Alexander Belchenko (bialix@ukr.net)
@version    0.9.devel
@date       2007/04/22
'''


__docformat__ = "javadoc"


from array import array
from binascii import hexlify, unhexlify


class IntelHex:
    ''' Intel HEX file reader. '''

    def __init__(self, source=None):
        ''' Constructor.

        @param  source      source for initialization
                            (file name of HEX file or file object)
        '''
        #public members
        self.padding = 0x0FF

        # private members
        self._buf = {}
        self._offset = 0

        if source is not None:
            if type(source) == type('') or hasattr(source, "read"):
                # load hex file
                self.loadhex(source)
            else:
                raise ValueError("source: bad initializer type")

    def decode_record(self, s, line=0, wrap64k=True):
        '''Decode one record of HEX file.

        @param  s       line with HEX record.
        @param  line    line number (for error messages).
        @param  wrap64k is decoder should wrap lowest 16-bit
                        of current address at 64K boundary.
                        By default address wrapped because
                        standard require this.
                        But some tools generate wrong hex files
                        (e.g. some Atmel AVR compilers),
                        so for this situation user can disable
                        address wrapping.

        @raise  EndOfFile   if EOF record encountered.
        '''
        s = s.rstrip('\r\n')
        if not s:
            return True       # empty line

        if s[0] == ':':
            try:
                bin = array('B', unhexlify(s[1:]))
            except TypeError:
                # this might be raised by unhexlify when odd hexascii digits
                raise BadHexRecord(line=line)
            length = len(bin)
            if length < 5:
                raise BadHexRecord(line=line)
        else:
            raise BadHexRecord(line=line)

        record_length = bin[0]
        if length != (5 + record_length):
            raise InvalidRecordLength(line=line)

        addr = bin[1]*256 + bin[2]

        record_type = bin[3]
        if not record_type in (0, 1, 2, 4):
            raise InvalidRecordType(line=line)

        crc = sum(bin)
        crc &= 0x0FF
        if crc != 0:
            raise InvalidRecordChecksum(line=line)

        if record_type == 0:
            # data record
            for i in xrange(4, 4+record_length):
                full_addr = addr + self._offset
                if not self._buf.get(full_addr, None) is None:
                    raise HexAddressOverlap(address=full_addr, line=line)
                self._buf[full_addr] = bin[i]
                addr += 1
                if wrap64k and addr == 65536:
                    addr = 0

        elif record_type == 1:
            # end of file record
            if record_length != 0:
                raise InvalidEOFRecord(line=line)
            raise EndOfFile

        elif record_type == 2:
            # Extended 8086 Segment Record
            if record_length != 2 or addr != 0:
                raise InvalidExtendedSegmentRecord(line=line)
            self._offset = (bin[4]*256 + bin[5]) * 16

        elif record_type == 4:
            # Extended Linear Address Record
            if record_length != 2 or addr != 0:
                raise InvalidExtendedLinearAddressRecord(line=line)
            self._offset = (bin[4]*256 + bin[5]) * 65536

    def loadhex(self, fobj, wrap64k=True):
        """Load hex file into internal buffer.

        @param  fobj        file name or file-like object
        @param  wrap64k     is lowest 16-bit of address should
                            wrap at 64K boundary
        """
        if not hasattr(fobj, "read"):
            fobj = file(fobj, "rU")
            fclose = fobj.close
        else:
            fclose = None

        self._offset = 0
        line = 0

        try:
            decode = self.decode_record
            try:
                for s in fobj:
                    line += 1
                    decode(s, line, wrap64k)
            except EndOfFile:
                pass
        finally:
            if fclose:
                fclose()

    def loadbin(self, fobj, offset=0):
        """Load bin file into internal buffer.

        @param  fobj        file name or file-like object
        @param  offset      starting address offset
        """
        raise NotImplementedError

    def loadfile(self, fobj, format):
        """Load data file into internal buffer.

        @param  fobj        file name or file-like object
        @param  format      file format ("hex" or "bin")
        """
        if format == "hex":
            self.loadhex(fobj)
        elif format == "bin":
            self.loadbin(fobj)
        else:
            raise ValueError('format should be either "hex" or "bin"')

    def _get_start_end(self, start=None, end=None):
        """Return default values for start and end if they are None
        """
        if start is None:
            start = min(self._buf.keys())
        if end is None:
            end = max(self._buf.keys())
        if start > end:
            start, end = end, start
        return start, end

    def tobinarray(self, start=None, end=None, pad=None):
        ''' Convert to binary form.
        @param  start   start address of output bytes.
        @param  end     end address of output bytes.
        @param  pad     fill empty spaces with this value
                        (if None used self.padding).
        @return         array of unsigned char data.
        '''
        if pad is None:
            pad = self.padding

        bin = array('B')

        if self._buf == {}:
            return bin

        start, end = self._get_start_end(start, end)

        for i in xrange(start, end+1):
            bin.append(self._buf.get(i, pad))

        return bin

    def tobinstr(self, start=None, end=None, pad=0xFF):
        ''' Convert to binary form.
        @param  start   start address of output bytes.
        @param  end     end address of output bytes.
        @param  pad     fill empty spaces with this value
                        (if None used self.padding).
        @return         string of binary data.
        '''
        return self.tobinarray(start, end, pad).tostring()

    def tobinfile(self, fobj, start=None, end=None, pad=0xFF):
        '''Convert to binary and write to file.

        @param  fobj    file name or file object for writing output bytes.
        @param  start   start address of output bytes.
        @param  end     end address of output bytes.
        @param  pad     fill empty spaces with this value
                        (if None used self.padding).
        '''
        if not hasattr(fobj, "write"):
            fobj = file(fobj, "wb")
            close_fd = True
        else:
            close_fd = False

        fobj.write(self.tobinstr(start, end, pad))

        if close_fd:
            fobj.close()

    def minaddr(self):
        ''' Get minimal address of HEX content. '''
        aa = self._buf.keys()
        if aa == []:
            return 0
        else:
            return min(aa)

    def maxaddr(self):
        ''' Get maximal address of HEX content. '''
        aa = self._buf.keys()
        if aa == []:
            return 0
        else:
            return max(aa)

    def __getitem__(self, addr):
        ''' Get byte from address.
        @param  addr    address of byte.
        @return         byte if address exists in HEX file, or self.padding
                        if no data found.
        '''
        return self._buf.get(addr, self.padding)

    def __setitem__(self, addr, byte):
        self._buf[addr] = byte

    def writefile(self, f):
        """Write data to file f in HEX format.
        @return True    if successful.
        """
        if hasattr(f, "write"):
            fobj = f
            close_fd = False
        else:
            fobj = file(f, 'w')
            close_fd = True

        minaddr = IntelHex.minaddr(self)
        maxaddr = IntelHex.maxaddr(self)
        if maxaddr > 65535:
            offset = (minaddr/65536)*65536
        else:
            offset = None

        while True:
            if offset != None:
                # emit 32-bit offset record
                high_ofs = offset / 65536
                offset_record = ":02000004%04X" % high_ofs
                bytes = divmod(high_ofs, 256)
                csum = 2 + 4 + bytes[0] + bytes[1]
                csum = (-csum) & 0x0FF
                offset_record += "%02X\n" % csum 

                ofs = offset
                if (ofs + 65536) > maxaddr:
                    rng = xrange(maxaddr - ofs + 1)
                else:
                    rng = xrange(65536)
            else:
                ofs = 0
                offset_record = ''
                rng = xrange(maxaddr + 1)

            csum = 0
            k = 0
            record = ""
            for addr in rng:
                byte = self._buf.get(ofs+addr, None)
                if byte != None:
                    if k == 0:
                        # optionally offset record
                        fobj.write(offset_record)
                        offset_record = ''
                        # start data record
                        record += "%04X00" % addr
                        bytes = divmod(addr, 256)
                        csum = bytes[0] + bytes[1]

                    k += 1
                    # continue data in record
                    record += "%02X" % byte
                    csum += byte

                    # check for length of record
                    if k < 16:
                        continue

                if k != 0:
                    # close record
                    csum += k
                    csum = (-csum) & 0x0FF
                    record += "%02X" % csum
                    fobj.write(":%02X%s\n" % (k, record))
                    # cleanup
                    csum = 0
                    k = 0
                    record = ""
            else:
                if k != 0:
                    # close record
                    csum += k
                    csum = (-csum) & 0x0FF
                    record += "%02X" % csum
                    fobj.write(":%02X%s\n" % (k, record))

            # advance offset
            if offset is None:
                break

            offset += 65536
            if offset > maxaddr:
                break

        # end-of-file record
        fobj.write(":00000001FF\n")
        if close_fd:
            fobj.close()
#/IntelHex


class IntelHex16bit(IntelHex):
    """Access to data as 16-bit words."""

    def __init__(self, source):
        """Construct class from HEX file
        or from instance of ordinary IntelHex class.

        @param  source  file name of HEX file or file object
                        or instance of ordinary IntelHex class
        """
        if isinstance(source, IntelHex):
            # from ihex8
            self.Error = source.Error
            self.AddrOverlap = source.AddrOverlap
            self.padding = source.padding
    
            # private members
            self._fname = source._fname
            self._buf = source._buf
            self._readed = source._readed
            self._eof = source._eof
            self._offset = source._offset
        else:
            IntelHex.__init__(self, source)

        if self.padding == 0x0FF:
            self.padding = 0x0FFFF

    def __getitem__(self, addr16):
        """Get 16-bit word from address.
        Raise error if found only one byte from pair.

        @param  addr16  address of word (addr8 = 2 * addr16).
        @return         word if bytes exists in HEX file, or self.padding
                        if no data found.
        """
        addr1 = addr16 * 2
        addr2 = addr1 + 1
        byte1 = self._buf.get(addr1, None)
        byte2 = self._buf.get(addr2, None)

        if byte1 != None and byte2 != None:
            return byte1 | (byte2 << 8)     # low endian

        if byte1 == None and byte2 == None:
            return self.padding

        raise Exception, 'Bad access in 16-bit mode (not enough data)'

    def __setitem__(self, addr16, word):
        addr_byte = addr16 * 2
        bytes = divmod(word, 256)
        self._buf[addr_byte] = bytes[1]
        self._buf[addr_byte+1] = bytes[0]

    def minaddr(self):
        '''Get minimal address of HEX content in 16-bit mode.'''
        aa = self._buf.keys()
        if aa == []:
            return 0
        else:
            return min(aa)/2

    def maxaddr(self):
        '''Get maximal address of HEX content in 16-bit mode.'''
        aa = self._buf.keys()
        if aa == []:
            return 0
        else:
            return max(aa)/2

#/class IntelHex16bit


def hex2bin(fin, fout, start=None, end=None, size=None, pad=0xFF):
    """Hex-to-Bin convertor engine.
    @return     0   if all OK

    @param  fin     input hex file (filename or file-like object)
    @param  fout    output bin file (filename or file-like object)
    @param  start   start of address range (optional)
    @param  end     end of address range (optional)
    @param  size    size of resulting file (in bytes) (optional)
    @param  pad     padding byte (optional)
    """
    h = IntelHex(fin)
    if not h.readfile():
        print "Bad HEX file"
        return 1

    # start, end, size
    if size != None and size != 0:
        if end == None:
            if start == None:
                start = h.minaddr()
            end = start + size - 1
        else:
            if (end+1) >= size:
                start = end + 1 - size
            else:
                start = 0

    try:
        h.tobinfile(fout, start, end, pad)
    except IOError:
        print "Could not write to file: %s" % fout
        return 1

    return 0
#/def hex2bin


##
# Custom Errors

class IntelHexError(StandardError):
    '''Base Exception class for IntelHex module'''

    def __init__(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)

    def __str__(self):
        try:
            # __str__() should always return a 'str' object
            # never a 'unicode' object.
            s = self.__doc__ % self.__dict__
            if isinstance(s, unicode):
                return s.encode('utf8')
            return s
        except (NameError, ValueError, KeyError), e:
            return 'Unprintable exception %s: %s' \
                % (self.__class__.__name__, str(e))

class EndOfFile(IntelHexError):
    '''EOF record reached -- signal to stop read file'''

class HexReaderError(IntelHexError):
    '''Generic error of reading HEX file'''

class NotAHexFile(HexReaderError):
    '''File "%(filename)s" is not a valid HEX file'''

class BadHexRecord(HexReaderError):
    '''Hex file contains invalid record at line %(line)d'''

class InvalidRecordLength(BadHexRecord):
    '''Record at line %(line)d has invalid length'''

class InvalidRecordType(BadHexRecord):
    '''Record at line %(line)d has invalid record type'''

class InvalidRecordChecksum(BadHexRecord):
    '''Record at line %(line)d has invalid checksum'''

class InvalidEOFRecord(BadHexRecord):
    '''File has invalid End-of-File record'''

class InvalidExtendedSegmentRecord(BadHexRecord):
    '''Invalid Extended 8086 Segment Record at line %(line)d'''

class InvalidExtendedLinearAddressRecord(BadHexRecord):
    '''Invalid Extended Linear Address Record at line %(line)d'''

class HexAddressOverlap(HexReaderError):
    '''Hex file has address overlap at address 0x%(address)X on line %(line)d'''


##
# MAIN
if __name__ == '__main__':
    import getopt
    import os
    import sys

    usage = '''Hex2Bin python converting utility.
Usage:
    python intelhex.py [options] file.hex [out.bin]

Arguments:
    file.hex                name of hex file to processing.
    out.bin                 name of output file.
                            If omitted then output write to file.bin.

Options:
    -h, --help              this help message.
    -p, --pad=FF            pad byte for empty spaces (ascii hex value).
    -r, --range=START:END   specify address range for writing output
                            (ascii hex value).
                            Range can be in form 'START:' or ':END'.
    -l, --length=NNNN,
    -s, --size=NNNN         size of output (decimal value).
'''

    pad = 0xFF
    start = None
    end = None
    size = None

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hp:r:l:s:",
                                  ["help", "pad=", "range=",
                                   "length=", "size="])

        for o, a in opts:
            if o in ("-h", "--help"):
                print usage
                sys.exit(0)
            elif o in ("-p", "--pad"):
                try:
                    pad = int(a, 16) & 0x0FF
                except:
                    raise getopt.GetoptError, 'Bad pad value'
            elif o in ("-r", "--range"):
                try:
                    l = a.split(":")
                    if l[0] != '':
                        start = int(l[0], 16)
                    if l[1] != '':
                        end = int(l[1], 16)
                except:
                    raise getopt.GetoptError, 'Bad range value(s)'
            elif o in ("-l", "--lenght", "-s", "--size"):
                try:
                    size = int(a, 10)
                except:
                    raise getopt.GetoptError, 'Bad size value'

        if start != None and end != None and size != None:
            raise getopt.GetoptError, 'Cannot specify START:END and SIZE simultaneously'

        if not args:
            raise getopt.GetoptError, 'Hex file is not specified'

        if len(args) > 2:
            raise getopt.GetoptError, 'Too many arguments'

    except getopt.GetoptError, msg:
        print msg
        print usage
        sys.exit(2)

    fin = args[0]
    if len(args) == 1:
        import os.path
        name, ext = os.path.splitext(fin)
        fout = name + ".bin"
    else:
        fout = args[1]

    if not os.path.isfile(fin):
        print "File not found"
        sys.exit(1)

    sys.exit(hex2bin(fin, fout, start, end, size, pad))
