# UrchinSec CTF

### Challenge - By Polar RSA 
#### Points: 250

A python file and a file containing the ciphertext were provided. The python code shows how the encryption that produced the ciphertext was done. There are 3 functions , The first generates a prime number, the second function (g_rsa_pair) generates the key pair given a key size, that last function does the encryption


```python
from Crypto.Util.number import getPrime as gp , bytes_to_long as btl
import random as rd
import sympy.ntheory as nt

def g_prime(bit_length):
    return gp(bit_length)

def g_rsa_pair(bit_length):
    p = g_prime(bit_length)
    q = nt.nextprime(p)
    x, y = 1337, 5000
    for _ in range(rd.randint(x, y)):
        q = nt.nextprime(q)
    N = p * q
    phi_N = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi_N)  
    public_key = (N, e)
    private_key = (N, d)
    return public_key, private_key # N, e     N,d

def enryption(message, public_key):
    N, e = public_key
    pt = btl(message.encode())
    ct = pow(pt, e, N)
    return ct

bit_length = 1024
print("start")
print(g_rsa_pair(bit_length))
public_key, _ = g_rsa_pair(bit_length)
print(public_key)
msg = "urchinsec{Fake_Flag}"
ciphertext = enryption(msg, public_key)
print(f"n: {public_key[0]}")
print(f"e: {public_key[1]}")
print(f"cipher: {ciphertext}")
```


Examining the Python file, our attention can be directed towards the process of generating the RSA key pair.


```python
def g_rsa_pair(bit_length):
    p = g_prime(bit_length)
    q = nt.nextprime(p)
    x, y = 1337, 5000
    for _ in range(rd.randint(x, y)):
        q = nt.nextprime(q)
    N = p * q
    phi_N = (p - 1) * (q - 1)
    e = 65537
    d = pow(e, -1, phi_N)  
    public_key = (N, e)
    private_key = (N, d)
    return public_key, private_key # N, e     N,d

```
Let's delve into the generation process of p and q:

The get_prime() function is utilized to obtain a prime number, p. Subsequently, q is generated through the expression "q = nt.nextprime(p)", Reading the library documentation of nextprime function (<a href="https://docs.sympy.org/latest/modules/ntheory.html#sympy.ntheory.generate.nextprime">here</a>), It says the function generates the next prime number greater than the argunment given to it, as p was the argument given to it, we can see that the next couple of prime numbers after p was assigned to q. from here we can deduce the diffrence between p and q is negligible.

Now, where is the problem in that, RSA encryption algorithm relies on the fact that factorization of large numbers is a very hard problem. In our own case, two prime numbers were chosen p, q, the multiplication of both numbers will be made publicly assessible, N=p*q, the security of this encryption algorithm is the fact that given N, a user will find it impossible to generate p and q without bruteforcing. However, vulnerable implementations of this could lead to it being broken, one of the occurence is in situations where p and q are really close as in our case here, This can lead to the public key being broken with Fermat factorization algorithm. 

Fermat says the product of two large primes can always be written as N=(a-b)(a+b), with a being the middle between the two primes and b the distance from the middle to each of the primes.
If the primes are close then a is close to the square root of N. This allows guessing the value a by starting with the square root of N and then incrementing the guess by one each round.
For each guess we can calculate b^2 = a^2 - N. If the result is a square we know we have guessed a correctly. From this we can calculate p=a+b and q=a-b. Hence get back p and q.


### Factorizing N using farmat equatiom

```
import gmpy2

N = 13660434380581469341975259828359442143257638335184201302273368295115642264434078009719568658893902099636280367748794936198883121916566759980319478068451889149773226303724397129080256671084001239425357663205345604232700769511136087038814886708523857954047161710079081105648157438922135347302268392557280337962501293170357378150549402374842219641781167567899043267569898951833055690878240668548807574813621152068811079565478546974052540054707402886449015640286146318337170863094022162781259688095263640720121736648132174258723707789668493418719055328110579315482197651253358684859047225130074022770557785786256404214699

def fermat_factor(n):
    assert n % 2 != 0

    a = gmpy2.isqrt(n)
    b2 = gmpy2.square(a) - n

    while not gmpy2.is_square(b2):
        a += 1
        b2 = gmpy2.square(a) - n

    p = a + gmpy2.isqrt(b2)
    q = a - gmpy2.isqrt(b2)

    return int(p), int(q)

if __name__ == "__main__":
    (p, q) = fermat_factor(N)



```
Hence our p and q



### Honey Sea 


```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import os
import binascii

def generate_key():
    return os.urandom(16)

def generate_iv():
    return os.urandom(16)

def encrypt_flag(flag, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted = cipher.encrypt(pad(flag.encode(), 16))
    return encrypted

def generate_signature(iv, key):
    signature_bytes = [a ^ b for a, b in zip(iv, key[::-1])]
    signature_hex = binascii.hexlify(bytearray(signature_bytes)).decode()
    return signature_hex

def encrypt_flag_with_signature(flag, key, iv):
    encrypted_data = encrypt_flag(flag, key, iv)
    signature = generate_signature(iv, key)
    iv_hex = iv.hex()[4:] 
    encrypted_hex = encrypted_data.hex()
    ciphertext = iv_hex + encrypted_hex + signature
    return {"cipher": ciphertext}

def main():
    FLAG = "urchinsec{Fake_Flag}"
    KEY = generate_key()
    IV = generate_iv()

    encrypted_flag = encrypt_flag_with_signature(FLAG, KEY, IV)
    print(encrypted_flag)

if __name__ == "__main__":
    main()

```

Walking back, we can see the "encrypt_flag_with_signature() takes in the flag, key and randomly generated iv and produce a ciphertext which contains the "iv_hex + encrypted_hex + signature" . The vulnerability arise from how the signature;

signature = iv + key

To generate the key, we just have to xor the signature and the IV that was given with the ciphertext. 

i.e key = iv + signature


The only issue here is the iv we have has its first two bytes removed. To generate the full iv , we have to bruteforce the first two bytes , given the lenght of the bruteforce is negligible we have nothing to worry about , once the key is derived we just have to decrypt

```py
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

```



## SANTAZIP

```python
zip_object = SantaZip("flag.txt", "flag.zip", password)
zip_object.generate_zip_file()
```

```python

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

```

To solve this challenge we have to understand how the python program is generating its zip, this way we can reverse the algorithm and solve the challenge. 
First, a salt of 16bytes was generated , then an initialization vector of 16 bytes was also generated , after which a password hash of 32 bytes was generated with the a key supplied by the user who generated the hash . The algorithm proceeded to encrypt the padded compressed input file with AES CBC, and finally write the salt, iv and ciphertext into a file.



```python
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
```
To reverse the algorithm, we have to extract the salt, iv and ciphertext in the order it was written to the file. then we have to generate the key(pass hash) from the password with the salt we extracted from file , after which we decrypt the file and strip the padded space and decompress
