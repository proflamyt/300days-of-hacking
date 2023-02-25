xor = []
p = []

enc = []

for i in range(len(xor)-1):
  p.append(xor[i] ^ xor[i+1]) 
  
  
for i in range(len(enc)):
  flag += p[i] ^ enc[i]
  
 
print(flag)
