from intelhex import IntelHexWord

h16 = IntelHexWord('test_16bit.hex', word_length=16)
#h16.loadhex('test_16bit.hex')
h16.write_hex_file('test_16bit.out.hex', byte_count=32)

print('{:x}'.format(h16[0x3F2132]))
