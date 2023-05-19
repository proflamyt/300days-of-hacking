from itertools import cycle

hex_str = '0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104'

byte_str = bytes.fromhex(hex_str)

plain = 'crypto{'

for i, j in zip(byte_str, plain):
   
    print(chr(i^ord(j)), end='')



guess_key = 'myXORkey'*len(byte_str)

for i, j in zip(byte_str, cycle('myXORkey')):
    print(chr(i^ord(j)), end='')