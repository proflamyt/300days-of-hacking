# Oracle 

import requests
import string
import binascii

URL = 'https://aes.cryptohack.org/ecb_oracle/encrypt/'
chunk_size = 32
alphanumeric = string.ascii_letters + string.digits + string.punctuation
_guess = 'ypto{p3n6u1n5_h' + 'ypto{p3n6u1n5_cr' # ypto{p3n6u1n5_r ead
guess = 'crypto{p3n6u1n5_'
i_guess = 'crypto{p3n6u1n5_'
num = 8
first_payload = binascii.hexlify(guess.encode()).decode()
resp = requests.get(f"{URL}/{first_payload }")
ciphertext_hex = resp.json()["ciphertext"]
#print(ciphertext_hex)
p = 1

while True:
    for i in range(33, 125):
        test = guess[p:] + chr(i)
        word = binascii.hexlify(test.encode()).decode()
        second_payload = binascii.hexlify(i_guess[p:].encode()).decode()
        resp = requests.get(f"{URL}/{word + second_payload}")
        ciphertext_hex = resp.json()["ciphertext"]
        if ciphertext_hex[:32] == ciphertext_hex[64:96]:
            guess += chr(i)
            print(guess)
            p += 1
            break
    print('no')



# print( # crypto{p3n6u1n5_
# print(ciphertext_hex[32:64]) # crypto{p3n6u1n5_
# print(ciphertext_hex[64:96]) # crypto{p3n6u1n5_
# print(ciphertext_hex[96:]) 

# AAAAAAAAAAAAAAAc AAAAAAAAAAAAAAAc rypto
# AAAAAAAAAAAAAAAc rypto{p3n6u1n5_c rypto{p3n6u1n5_r eminder0

# while True:
#     for i in range(33, 125):
#         test = guess + chr(i)
#         word = binascii.hexlify(test.encode()).decode()
#         first_payload = '41'*num + word 
#         second_payload = ''
#         resp = requests.get(f"{URL}/{first_payload + second_payload}")
#         ciphertext_hex = resp.json()["ciphertext"]
#         if ciphertext_hex[:32] == ciphertext_hex[32:64]:
#             num -= 1
#             guess += chr(i)
#             print(guess)
#             break
    
#     print('no')
