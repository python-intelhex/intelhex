import intelhex

ih = intelhex.IntelHex()
for i in range(65536): ih[i] = i & 0x0FF

print(len(ih))

print(ih.get_memory_size())
