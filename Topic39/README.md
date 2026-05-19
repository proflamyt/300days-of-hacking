---
title: "Cryptography"
topic: "cryptography"
tags: [cryptography, ecc, xor, modular-arithmetic, elliptic-curve, diffie-hellman, rsa]
difficulty: advanced
day: 39
layout: default
parent: Topics
nav_order: 39
---

# Cryptography

## What You Will Learn
- How ASCII, hex, and Base64 encoding work
- XOR properties and how they relate to encryption
- Modular arithmetic and why it powers modern crypto
- How Elliptic Curve Cryptography (ECC) works
- How Elliptic Curve Diffie-Hellman key exchange works

## Key Concepts

### Encoding Basics

**ASCII** is a 7-bit encoding used to represent characters in the alphabet. Characters are represented by integers between 0 and 127.

In Python, `chr()` converts an ASCII number to a character, and `ord()` converts a character to an ASCII number.

Hexadecimal can represent ASCII strings. Each letter is converted to its ASCII number, then to base-16. These can be combined into one long hex string.

Using `bytes.fromhex()`, each hex value is converted to its decimal equivalent, then to its byte (8-bit) representation which can be turned back into ASCII.

**Base64** encodes bytes as an ASCII string in a format that is safe to transmit over networks. One Base64 character encodes 6 bits.

### XOR

XOR is a bitwise operator which returns 0 if the bits are the same, and 1 otherwise.

**XOR Properties** (`⊕` = XOR):

```
Commutative:  A ⊕ B = B ⊕ A
Associative:  A ⊕ (B ⊕ C) = (A ⊕ B) ⊕ C
Identity:     A ⊕ 0 = A
Self-Inverse: A ⊕ A = 0
```

XOR encryption is simple: `ciphertext = plaintext ⊕ key`. Decryption uses the same operation: `plaintext = ciphertext ⊕ key`.

### Trapdoor Functions

Trapdoor functions allow a client to keep data secret by performing a mathematical operation that is easy to compute in one direction, but very hard to reverse. Asymmetric crypto (RSA, ECC) is built on trapdoor functions.

## Modular Arithmetic

### The Quotient Remainder Theorem

For any integer A and positive integer B, there exist unique integers Q and R such that:

```
A = B * Q + R    where 0 ≤ R < B

Example: 9 = 4 * 2 + 1, so 9 % 4 = 1
```

### Modular Operations

```
(A + B) mod C = (A mod C + B mod C) mod C
(A - B) mod C = (A mod C - B mod C) mod C
(A * B) mod C = (A mod C * B mod C) mod C
A^B mod C     = ((A mod C)^B) mod C
```

### GCD and Euclidean Algorithm

The **Greatest Common Divisor (GCD)** is the largest number that divides two positive integers. The Euclidean algorithm finds it efficiently by replacing the larger number with the remainder when divided by the smaller.

```
gcd(252, 105):
252 % 105 = 42
105 % 42  = 21
42  % 21  = 0
=> GCD = 21
```

### Extended Euclidean Algorithm

Computes integers p, q such that `px + qy = gcd(a, b)`. Used to find **modular inverses**.

### Modular Inverse

An integer `a` has an inverse modulo `n` only if `gcd(a, n) = 1`.

```
Does the modular inverse of 2 mod 5 exist?
gcd(2, 5) == 1 → yes, the modular inverse exists.
```

### Chinese Remainder Theorem

Determines a number `p` that, when divided by given divisors, leaves given remainders. Widely used in RSA optimizations.

### Quadratic Residue

A number `x` (between 1 and p−1) is a **quadratic residue** modulo prime `p` if there exists a `y` such that `y² ≡ x (mod p)`. The **Legendre Symbol** is a fast way to test this.

## Elliptic Curve Cryptography (ECC)

**Terms:**
- **Group order**: How many unique positions exist before you cycle back to the start
- **Finite Fields**: Numbers wrapped around after some modulus `p`

### Point Addition

Elliptic curve addition means drawing a line between two points and finding the third intersection point, then reflecting it over the x-axis.

```python
p = 9739
a = 497
b = 1768

def inverse_mod(k, p):
    return pow(k, -1, p)

def point_add(P, Q):
    if P == "O":
        return Q
    if Q == "O":
        return P
    (x1, y1) = P
    (x2, y2) = Q
    if x1 == x2 and y1 != y2:
        return "O"
    
    if P != Q:
        m = ((y2 - y1) * inverse_mod(x2 - x1, p)) % p
    else:
        # Point doubling
        m = ((3 * x1**2 + a) * inverse_mod(2 * y1, p)) % p
    
    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)

P = (493, 5564)
Q = (1539, 4742)
R = (4403, 5202)

S1 = point_add(P, P)      # 2P
S2 = point_add(S1, Q)     # 2P + Q
S  = point_add(S2, R)     # 2P + Q + R
print("S =", S)
```

## Elliptic Curve Diffie-Hellman (ECDH)

Key exchange using elliptic curves:
1. Alice generates secret `nA` and calculates `Qa = [nA]G`
2. Bob generates secret `nB` and calculates `Qb = [nB]G`
3. They exchange `Qa` and `Qb`
4. Alice computes `[nA]Qb`, Bob computes `[nB]Qa`
5. Both arrive at the same shared secret: `S = [nA]Qb = [nB]Qa`

### Elliptic Curve Signature

- Bob generates private key `n` and public key `Qb = nG`
- Bob signs message `M` with random value `k`: `r = k·G`, `s = k⁻¹(H(M) + r·n)`
- Signature is `(r, s)` and public key is `Qb`
- **If `k` is reused or leaked**, an attacker can compute the private key: `n = r⁻¹(s·k - H(M))`

## Resources

- [CryptoHack — Crypto Challenges](https://cryptohack.org/)
- [Wikipedia — Euclidean Algorithm](https://en.wikipedia.org/wiki/Euclidean_algorithm)
- [Khan Academy — Modular Arithmetic](https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/what-is-modular-arithmetic)
- [Brilliant — Chinese Remainder Theorem](https://brilliant.org/wiki/chinese-remainder-theorem/)
- [YouTube — Elliptic Curve Cryptography](https://www.youtube.com/watch?v=RdP7_hMUTn0)
