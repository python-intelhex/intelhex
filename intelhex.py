#!/usr/bin/python
# Intel HEX file format reader and converter.

'''Intel HEX file format reader and converter.

This script also may be used as hex2bin convertor utility.

@author     Alexander Belchenko (bialix@ukr.net)
@version    0.8
@date       2006/03/29
'''


__docformat__ = "javadoc"


import array


class IntelHex:
    ''' Intel HEX file reader. '''

    def __init__(self, fname):
        ''' Constructor.
        @param  fname   file name of HEX file or file object.
        '''
        #public members
        self.Error = None
        self.AddrOverlap = None
        self.padding = 0x0FF

        # private members
        self._fname = fname
        self._buf = {}
        self._readed = False
        self._eof = False
        self._offset = 0

    def readfile(self):
        ''' Read file into internal buffer.
        @return True    if successful.
        '''
        if self._readed:
            return True

        if not hasattr(self._fname, "read"):
            f = file(self._fname, "rU")
        else:
            f = self._fname

        self._offset = 0
        self._eof = False

        while True:
            s = f.readline()
            if s == '':
                break

            if not self.decode_record(s):
                return False

            if self._eof:
                break

        self._readed = True
        return True

    def decode_record(self, s):
        ''' Decode one record of HEX file.
        @param  s       line with HEX record.
        @return True    if line decode OK, or this is not HEX line.
                False   if this is invalid HEX line or checksum error.
        '''
        s = s.rstrip('\r\n')
        len_ = len(s)
        if len_ == 0: return True       # empty line
        if s[0] != ':': return True     # first char must be ':'

        if len_ < 11:
            self.Error = "Too short line"
            return False

        record_length = int(s[1:3], 16)

        if len_ != (11 + record_length*2):
            self.Error = "Invalid line length"
            return False

        addr = int(s[3:7], 16)

        record_type = int(s[7:9], 16)
        if not record_type in (0, 1, 2, 4):
            self.Error = "Invalid type of record"
            return False

        data_bytes = [int(s[i:i+2], 16) for i in xrange(1,len_,2)]

        crc = reduce(lambda x, y: x+y, data_bytes, 0)
        crc &= 0x0FF
        if crc != 0:
            self.Error = "Invalid crc"
            return False

        if record_type == 0:
            # data record
            addr += self._offset
            for i in data_bytes[4:4+record_length]:
                if self._buf.get(addr, None) != None:
                    self.AddrOverlap = addr
                self._buf[addr] = i
                addr += 1       # FIXME: addr should be wrapped on 64K boundary

        elif record_type == 1:
            # end of file record
            if record_length != 0:
                self.Error = "Bad End-of-File Record"
                return False
            self._eof = True

        elif record_type == 2:
            # Extended 8086 Segment Record
            if record_length != 2 or addr != 0:
                self.Error = "Bad Extended 8086 Segment Record"
                return False
            self._offset = int(s[9:13], 16) << 4

        elif record_type == 4:
            # Extended Linear Address Record
            if record_length != 2 or addr != 0:
                self.Error = "Bad Extended Linear Address Record"
                return False
            self._offset = int(s[9:13], 16) << 16

        else:
            self.Error = "Invalid type of record"
            return False

        return True

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

        bin = array.array('B')

        addresses = self._buf.keys()
        if addresses == []:
            return bin

        if start is None:
            start = min(addresses)
        if end is None:
            end = max(addresses)

        if start > end:
            start, end = end, start

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
        bin = self.tobinarray(start, end, pad)
        return bin.tostring()

    def tobinfile(self, fname, start=None, end=None, pad=0xFF):
        ''' Convert to binary and write to fname file.
        @param  fname   file name or file object for write output bytes.
        @param  start   start address of output bytes.
        @param  end     end address of output bytes.
        @param  pad     fill empty spaces with this value
                        (if None used self.padding).
        @return         Nothing.
        '''
        bin = self.tobinarray(start, end, pad)
        if not hasattr(fname, "write"):
            fname = file(fname, "wb")
        bin.tofile(fname)

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
        else:
            fobj = file(f, 'w')

        maxaddr = IntelHex.maxaddr(self)
        if maxaddr > 65535:
            offset = 0
        else:
            offset = None

        while True:
            if offset != None:
                # emit 32-bit offset record
                high_ofs = offset / 65536
                offset_record = ":02000004%04X\n" % high_ofs
                bytes = divmod(high_ofs, 256)
                csum = 2 + 4 + bytes[0] + bytes[1]
                csum = (-csum) & 0x0FF
                fobj.write("%02X\n" % csum)

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

    sys.exit(hex2bin(fin, fout))
