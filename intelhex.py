#!/usr/bin/python
# @file     intelhex.py
# @brief    Work with Intel HEX file format
# @author   Alexander Belchenko, 2005

'''
Intel HEX file format reader and converter.
'''


class IntelHex:
    ''' Intel HEX file reader. '''

    def __init__(self, fname):
        ''' Constructor.
        @param  fname   file name of HEX file or file-like object.
        '''
        self._fname = fname
        self._buf = {}
        self._readed = False
        self.Error = None
        self.Intersection = None
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
        @return False   if this is invalid HEX line or checksum error.
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
                    self.Intersection = aaaa
                self._buf[aaaa] = i
                aaaa += 1
        elif tt == 1:
            # end of file record
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

    def tobin(self, start=None, end=None, fill=0xFF):
        ''' Convert to binary form.
        @param  start   start address of output bytes.
        @param  end     end address of output bytes.
        @param  fill    fill empty spaces with this value.
        @return string with binary data.
        '''
        aa = self._buf.keys()
        aa.sort()
        if aa == []:    return ''
        amin = aa[0]
        amax = aa[-1]
        if start is None:
            start = amin
        if end is None:
            end = amax

        s = ''
        for i in xrange(start, end+1, 1):
            s += chr(self._buf.get(i, fill))

        return s

    def tobinfile(self, fname, start=None, end=None, fill=0xFF):
        ''' Convert to binary and write to fname file.
        @param  fname   file name for write output bytes.
        @param  start   start address of output bytes.
        @param  end     end address of output bytes.
        @param  fill    fill empty spaces with this value.
        @return string with binary data.
        '''
        f = file(fname, "wb")
        f.write(self.tobin(start, end, fill))
        f.close()


if __name__ == '__main__':
    h = IntelHex('hello.hex')
    print h.readfile()
    print len(h._buf)

    h.tobinfile("1.bin")

