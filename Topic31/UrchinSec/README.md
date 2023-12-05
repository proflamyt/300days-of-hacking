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

