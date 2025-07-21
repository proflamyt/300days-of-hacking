import re

with open('output.txt') as file:
  xor = file.readline()
  enc = file.readline()

xor_values = [int(x) for x in re.findall(r'\d+', xor)]
enc_values = [int(x) for x in re.findall(r'\d+', enc)]

print(xor_values)

real_pass = []


flag = ''

for i in range(len(xor_values)-1):
  real_pass.append(xor_values[i] ^ xor_values[i+1]) 
  
real_pass.insert(0, 124)

for i in range(len(enc_values)):
  flag += chr(real_pass[i] ^ enc_values[i])
  
 
print(flag)
