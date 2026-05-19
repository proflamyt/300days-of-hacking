---
title: "Encryption"
topic: "encryption"
tags: [encryption, cryptography, rsa, aes, xor, gpg, openssl, diffie-hellman]
difficulty: intermediate
day: 10
layout: default
parent: Topics
nav_order: 10
---

# Cryptography

## What You Will Learn
- What cryptography is and why it matters in security
- The difference between symmetric and asymmetric encryption
- How RSA works, step by step
- How XOR encryption works and why it's a building block for crypto
- How to use GPG and OpenSSL for practical encryption

A person who has previously never heard of the word "cryptography" may imagine it is a tough word to crack — but it isn't! A simple definition was given by the credible cybersecurity company Kaspersky: it defines cryptography as the study of secure communications techniques that allow only the sender and the intended recipient of a message to view its content.

## Encryption

Cryptography is closely related to encryption, which is a method of ensuring information is communicated securely by **encrypting** the original information into **ciphertext** and **decrypting** the ciphertext upon arrival for the intended recipient. This ensures that if any external party (a hacker eavesdropping) attempts to read the information, they would only see meaningless characters and would be unable to decipher the real message.

An example of cryptography is **Asymmetric Cryptography**:

Asymmetric cryptography uses a pair of mathematically generated keys to encrypt and decrypt data. Effective security requires keeping the private key private; the public key can be openly distributed without compromising security. Let us imagine the private and public key pair as a padlock and its key.

Here the padlock is the public key and its key is the private key. Mr. Ola in Nigeria wants to send Mr. cHow in the US a secret message by road. The road is dangerous and filled with spies who would like to read or tamper with the message. Mr. Ola and Mr. cHow must devise a way to send this message securely.

Mr. cHow buys a padlock with its key. This padlock is very secure — it can only be opened by the key that Mr. cHow holds. Now, Mr. cHow sends Mr. Ola the padlock, while keeping the only key.

Mr. Ola gets this padlock, gets a box, puts his message inside, and locks it with the padlock Mr. cHow sent him. Now no one can open this box without the key — not even Mr. Ola who locked it.

Mr. Ola sends this locked box through the insecure road to Mr. cHow, who is the only one who has the key to unlock it. Even if the box is intercepted by spies, the message remains safe.

The above example gives you a perfect understanding of how asymmetric encryption works.

Asymmetric cryptography can also be used for **digital signing** (which is quite the opposite of the above example). Digital signing means the private key is used for signing the data and it can be verified by anyone who has access to the public key. This ensures the data has not been tampered with and proves it came from the owner of the private key.

Consider this example:

Mr. cHow is a valuable asset and wants to remain anonymous, but he wants to deliver messages to his friends without showing up. The problem is that anytime he sends a message, they hardly believe it came from him. And bad guys are capitalizing on the trust by impersonating him — sometimes changing his messages, sometimes crafting fake messages demanding cash.

As a genius, Mr. cHow came up with a plan: he signs the messages he sends. He gets a padlock and its key — only this time he sends the **keys** out to everyone but keeps the **padlock**. He locks the messages he wants to send with his padlock (remember, only he has this padlock), then sends the padlocked messages out. Anytime his friends receive a message and want to confirm it came from Mr. cHow, all they do is use the key he sent them earlier to unlock it. If it opens, it really came from Mr. cHow.

I believe by now you have a broader idea of how cryptography works!


## Types of Symmetric Encryption

### Block Cipher Symmetric Encryption Algorithms

A block cipher converts the input (plaintext) into blocks and encrypts each block.

1. **AES** — Advanced Encryption Standard
2. **IDEA** — International Data Encryption Algorithm
3. **3DES** — Triple DES (Data Encryption Standard). Note: 3DES was deprecated in 2023.
4. **CAST5** — Also known as CAST-128
5. **Blowfish** — Designed by Bruce Schneier
6. **Twofish** — Designed by Bruce Schneier, derived from Blowfish
7. **CAMELLIA128, CAMELLIA192, and CAMELLIA256**

### Stream Ciphers

Stream ciphers encrypt the plaintext byte by byte.

### Encryption Using GPG

```bash
# Encrypt a file
gpg --symmetric --cipher-algo CIPHER message.txt

# Decrypt a file
gpg --output original_message.txt --decrypt message.gpg
```

### Encryption Using OpenSSL

```bash
# Encrypt
openssl aes-256-cbc -e -in message.txt -out encrypted_message

# Decrypt
openssl aes-256-cbc -d -in encrypted_message -out original_message.txt
```

## Asymmetric Encryption

### RSA

RSA gets its name from its inventors: Rivest, Shamir, and Adleman. It relies on the difficulty of factoring large prime numbers.

How it works:

1. Bob chooses two prime numbers: `p = 157` and `q = 199`. He calculates `N = 31243`.
2. With `φ(N) = N − p − q + 1 = 30888`, Bob selects `e = 163` and `d = 379` where `e × d mod φ(N) = 1`.
3. The public key is `(31243, 163)` and the private key is `(31243, 379)`.
4. Alice encrypts `x = 13`: `y = x^e mod N = 13^163 mod 31243 = 16342`.
5. Bob decrypts: `x = y^d mod N = 16342^379 mod 31243 = 13`.

```bash
# Generate private key and store in private-key.pem
openssl genrsa -out private-key.pem 2048

# Generate the public key from the private key
openssl rsa -in private-key.pem -pubout -out public-key.pem

# Encrypt with public key
openssl pkeyutl -encrypt -in plaintext.txt -out ciphertext -inkey public-key.pem -pubin

# Decrypt with private key
openssl pkeyutl -decrypt -in ciphertext -inkey private-key.pem -out decrypted.txt
```

## Diffie-Hellman

Diffie-Hellman (DH) is a key exchange protocol that allows two parties to establish a shared secret over an insecure channel without ever sending the secret itself. It is the foundation of TLS and many VPN protocols.

The math works like this:

1. Alice and Bob agree on a large prime `p` and a generator `g` (both public).
2. Alice picks a secret `a`, computes `A = g^a mod p`, and sends `A` to Bob.
3. Bob picks a secret `b`, computes `B = g^b mod p`, and sends `B` to Alice.
4. Alice computes `s = B^a mod p`. Bob computes `s = A^b mod p`. Both arrive at the same shared secret `s`.

## Public Key Infrastructure (PKI)

PKI is a framework for managing digital certificates and public-key encryption. It enables:

- **Certificate Authorities (CAs)**: Trusted entities that issue digital certificates.
- **Digital Certificates**: Bind a public key to an identity (used in HTTPS).
- **Certificate Chains**: A hierarchy of trust from root CA to end-entity certificate.

## XOR (Exclusive OR Cipher)

https://xor.pw/#

The XOR encryption algorithm is a very effective yet easy-to-implement method of symmetric encryption. XORing a message with a private key generates ciphertext that can be XORed again with the same key to recover the original text.

> Using a one-time pad:

```
olamide XOR private  = 0x1f1e081b081000
olamide XOR 0x1f1e081b081000 = private
private XOR 0x1f1e081b081000 = olamide
```

**Note:** Getting both the message and the ciphertext will reveal the private key. One-time pads are only secure if the key is as long as the message and never reused.

```python
# XOR Encryption Algorithm — www.101computing.net/xor-encryption-algorithm/

def binary(num, length=8):
    b = bin(num).lstrip("0b")
    b = "0" * (length - len(b)) + b
    return b

def hexa(num, length=2):
    h = hex(num).lstrip("0x").upper()
    h = "0" * (length - len(h)) + h
    return h

plaintext = input("Enter a message to encrypt:\n")
key = "101ComputingKey"
keyLength = len(key)
cipherAscii = ""
cipherDen = ""
cipherHex = ""
cipherBin = ""

for i in range(0, len(plaintext)):
    j = i % keyLength
    xor = ord(plaintext[i]) ^ ord(key[j])
    cipherAscii += chr(xor)
    cipherDen += str(xor) + " "
    cipherHex += hexa(xor) + " "
    cipherBin += binary(xor) + " "

print("\nCipher (Ascii form): \n" + cipherAscii)
print("\nCipher (Denary form): \n" + cipherDen)
print("\nCipher (Hexadecimal form): \n" + cipherHex)
print("\nCipher (Binary form): \n" + cipherBin)
```

## Resources

- [101computing.net — XOR Encryption](https://www.101computing.net/xor-encryption-algorithm/)
- [TryHackMe — Encryption Room](https://tryhackme.com/room/encryptioncrypto101)
- [OpenSSL Documentation](https://www.openssl.org/docs/)
- [Kaspersky — What is Cryptography?](https://www.kaspersky.com/resource-center/definitions/what-is-cryptography)
