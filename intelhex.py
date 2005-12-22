#!/usr/bin/python
# Intel HEX file format reader and converter.

'''\
Intel HEX file format reader and converter.

This script also may be used as hex2bin convertor utility.

@author     Alexander Belchenko (bialix@ukr.net)
@version    0.5
@date       2005/06/26
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
        l = len(s)
        if l == 0:  return True         # empty line
        if s[0] != ':': return True     # first char must be ':'
        if l < 11:
            self.Error = "Too short line"
            return False
        ll = int(s[1:3], 16)
        if l != (11 + ll*2):
            self.Error = "Invalid line length"
            return False
        aaaa = int(s[3:7], 16)
        tt = int(s[7:9], 16)
        if not tt in (0, 1, 2, 4):
            self.Error = "Invalid type of record"
            return False

        bb = [int(s[i:i+2], 16) for i in xrange(1,l,2)]
        crc = reduce(lambda x, y: x+y, bb, 0)
        crc &= 0x0FF
        if crc != 0:
            self.Error = "Invalid crc"
            return False

        if tt == 0:
            # data record
            aaaa = self._offset + aaaa
            for i in bb[4:4+ll]:
                if self._buf.get(aaaa, None) is not None:
                    self.AddrOverlap = aaaa
                self._buf[aaaa] = i
                aaaa += 1
        elif tt == 1:
            # end of file record
            if ll != 0:
                self.Error = "Bad End-of-File Record"
                return False
            self._eof = True
        elif tt == 2:
            # Extended 8086 Segment Record
            if ll != 2 or aaaa != 0:
                self.Error = "Bad Extended 8086 Segment Record"
                return False
            self._offset = int(s[9:13], 16) << 4
        elif tt == 4:
            # Extended Linear Address Record
            if ll != 2 or aaaa != 0:
                self.Error = "Bad Extended Linear Address Record"
                return False
            self._offset = int(s[9:13], 16) << 16
        else:
            # this is impossible
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

        aa = self._buf.keys()
        if aa == []:    return bin

        if start is None:
            start = min(aa)
        if end is None:
            end = max(aa)

        if start > end:
            start, end = end, start

        for i in xrange(start, end+1, 1):
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

#/IntelHex


if __name__ == '__main__':
    import sys, getopt, time

    usage = '''
Hex2Bin python converting utility.
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
        print >>sys.stderr, msg
        print >>sys.stderr, usage
        sys.exit(3)

    fin = args[0]
    if len(args) == 1:
        import os.path
        name, ext = os.path.splitext(fin)
        fout = name + ".bin"
    else:
        fout = args[1]

    h = IntelHex(fin)
    if not h.readfile():
        print >>sys.stderr, "Bad HEX file"
        sys.exit(1)

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
        print >>sys.stderr, "Could not write to file: %s" % fout
        sys.exit(2)

    sys.exit(0)
