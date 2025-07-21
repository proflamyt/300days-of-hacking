import requests
import hashlib
import json
from Crypto.Cipher import AES
import binascii

URL = 'https://aes.cryptohack.org'

resp = requests.get(f"{URL}/passwords_as_keys/encrypt_flag/")
ciphertext_hex = resp.json()["ciphertext"]




def main():
    with open("words") as f:
        for keyword in f.readlines():
            hash = hashlib.md5(keyword.strip().encode()).digest()
            ciphertext = bytes.fromhex(ciphertext_hex)
            cipher = AES.new(hash, AES.MODE_ECB)
            try:
                decrypted = cipher.decrypt(ciphertext)
                if decrypted.startswith(b'crypto{'):
                    print("key is %s" % keyword)
                    print(decrypted.decode('utf-8'))
                    break
            except ValueError as e:
                continue
            

            


if __name__ == '__main__':
    main()

# import requests
# import hashlib
# import json


# URL = 'https://aes.cryptohack.org'

# resp = requests.get(f"{URL}/passwords_as_keys/encrypt_flag/")
# cipher = json.loads(resp.text)['ciphertext']


# def main():
#     with open("words") as f:
#         for keyword in f.readlines():
#             key = hashlib.md5(keyword.strip().encode()).digest().hex()
#             response = requests.get(f"{URL}/passwords_as_keys/decrypt/{cipher}/{str(key)}")
#             resp = response.json()['plaintext']
#             print(resp)

#             if b'cryp' in bytes.fromhex(resp):
#                 print(resp)
#                 break


# if __name__ == '__main__':
#     main()



