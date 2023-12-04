from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import os
import binascii
import itertools


ciphertext = '888fb84744ea0ea84165cf6418b07bd829cc2a695e7d5bb4acdae1179bac51f02486993c80c028b3350029c171819ad9166b78e998c87be7233a302b83f0ebe67f4684682c4b3798f42587173965'


iv = ciphertext[:28]


signature = ciphertext[-32:]


encrypted = ciphertext[28:len(ciphertext)-32]

assert(iv+encrypted+signature==ciphertext)




byte_values = [format(i, '02X') for i in range(256)]




def generate_signature(iv, signature):
    signature_bytes = bytes(bytearray([a ^ b for a, b in zip(iv, signature)]))
    
    return signature_bytes[::-1]



combinations = itertools.product(byte_values, repeat=2)


result = [''.join(combination) for combination in combinations]


for num in result:
	

	iv_bytes = bytes.fromhex(num + iv)
	signature_bytes = binascii.unhexlify(signature)

	key = generate_signature(iv_bytes, signature_bytes)
	
	cipher = AES.new(key, AES.MODE_CBC, iv_bytes)
	encrypted_flag = bytes.fromhex(encrypted)
	try:
		decrypted = unpad(cipher.decrypt(encrypted_flag), 16)
		if b"urchinsec" in decrypted:
			print(key)
			print(decrypted.decode())
	except:
		continue









