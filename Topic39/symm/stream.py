
import requests
import json


url = 'http://aes.cryptohack.org/symmetry/'

def encrypted_flag():
    r = requests.get(url + "encrypt_flag/")
    return r.json()['ciphertext']


def encrypt(plain, iv):
    r = requests.get(url + "encrypt/" + plain + "/" + iv + "/")
    return r.json()['ciphertext']


cipher = encrypted_flag()
iv = cipher[:32]
cip = cipher[32:]

ret = encrypt(cip, iv)
print(bytes.fromhex(ret))


