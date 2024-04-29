from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
import zlib
import struct
import gzip

class SantaZip(object):
    def __init__(self, file_to_zip, zip_output, password):
        self.file_to_zip = file_to_zip
        self.zip_output = zip_output
        self.password = password

    def generate_zip_file(self):
        try:
            password = self.password
            salt = get_random_bytes(16)
            iv = get_random_bytes(16)
            key = PBKDF2(password, salt, dkLen=32, count=1000000)

            cipher = AES.new(key, AES.MODE_CBC, iv)
            with open(self.file_to_zip, "rb") as input_file:
                plaintext = input_file.read()

            compressed_data = zlib.compress(plaintext)


            padded_data = compressed_data + b' ' * (16 - len(compressed_data) % 16)
            ciphertext = cipher.encrypt(padded_data)

            with open(self.zip_output, "wb") as output_file:
                output_file.write(salt)
                output_file.write(iv)
                output_file.write(ciphertext)
            
            return f"{self.file_to_zip} is zipped into {self.zip_output}"
        except Exception as e:
            return f"Error : {e}"

    def decrypt_zip_file(self):

 
        with open(self.zip_output, "rb") as input_f:
            out = input_f.read()

        with open(self.zip_output, "rb") as input_file:
            salt = input_file.read(16)
            iv = input_file.read(16)
            ciphertext = input_file.read()

        

        key = PBKDF2(self.password, salt, dkLen=32, count=1000000)

        

        cipher = AES.new(key, AES.MODE_CBC, iv)

        plain_padded = cipher.decrypt(ciphertext).strip(b" ")

        return zlib.decompress(plain_padded)

        # oll = b"\x1f\x8b\x08\x08"

        # with open("ola.zip", 'wb') as tola:
        #     tola.write(oll)
        #     tola.write(plain_padded)







