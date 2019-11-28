c=bytes.fromhex('FE 0F 00 00 00 08 01 FF F1 D1')
print(c)
aa = ''.join(['%02x' % b for b in c])
print(aa.upper())
m='9'
h='10'
cc=':'.join((m,h))
print(cc)