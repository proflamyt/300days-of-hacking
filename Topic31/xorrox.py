#!/usr/bin/env python3

import random

with open("flag.txt", "rb") as filp: # reads in the file 
    flag = filp.read().strip() # strips it 

key = [random.randint(1, 256) for _ in range(len(flag))] # generates keys

xorrox = []
enc = []
for i, v in enumerate(key):  # index and lists keys
    k = 1
    for j in range(i, 0, -1):
        k ^= key[j]
    xorrox.append(k)
    enc.append(flag[i] ^ v) # xor flag and index

with open("output.txt", "w") as filp:
    filp.write(f"{xorrox=}\n")
    filp.write(f"{enc=}\n")
