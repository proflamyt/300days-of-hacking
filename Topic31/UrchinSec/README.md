# UrchinSec CTF

### By Polar RSA 

A python file and a ciphertext was given, The challenge wants the ciphertext to be decrypted.

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


Going through the python file, we can see how the rsa key pair was generated 

The vulnerable function

```
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

Lets look at how p and q was generated 

get_prime() gets a prime number, p , and q was generated with "q = nt.nextprime(p)".  from the documentation the nextprime function generates the next prime number greater than the argunment given to it 

https://docs.sympy.org/latest/modules/ntheory.html#sympy.ntheory.generate.nextprime. from the above code we can see a prime number after a couple of range was assigned to q. from here we can deduce the diffrence between p and q is negligible 


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


### Honey Sea 


```
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

```
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

