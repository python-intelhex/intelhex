from  intelhex import IntelHexWord
import numpy as np
import struct


ih= IntelHexWord(word_length=16)

f_hex = open('foo.hex', 'w')

angle = np.linspace(0,2*np.pi*(8191.0/8192.0),8192)
sin_curve=np.uint16(np.sin(angle)*32767.0+32768.0)
for count,sini in enumerate(sin_curve):
    if count % 128 == 0:
        print(sini)
    ih[count]=sini

ih.write_hex_file(f_hex, byte_count=32)


f_hex.close()

bin = ih.tobinarray()
for count,bini in  enumerate(bin):
    if count % 128 == 0:
        print(bini)
