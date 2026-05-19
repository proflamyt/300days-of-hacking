---
title: "SageMath for Cryptography"
topic: "sagemath"
tags: [sagemath, mathematics, cryptography, elliptic-curves, modular-arithmetic, algebra]
difficulty: advanced
day: 86
layout: default
parent: Topics
nav_order: 86
---

# SageMath for Cryptography

## What You Will Learn
- How to use SageMath to solve algebraic equations
- How to work with matrices and finite fields
- How SageMath is used for cryptographic challenges
- Practical examples of polynomial and linear equation solving

## What Is It?

**SageMath** is a free open-source mathematics software system built on Python. It is widely used in cryptography research and CTF competitions for:
- Solving equations and systems of equations
- Modular arithmetic and number theory
- Elliptic curve computations
- Matrix operations over finite fields

SageMath is an essential tool for **CryptoHack** challenges and CTF crypto problems.

## Why It Matters

Many crypto CTF challenges require solving mathematical problems that are impractical to do by hand. SageMath makes it easy to work with:
- Large prime numbers
- Finite fields (`GF(p)`)
- Polynomial equations
- Lattice-based problems

## Single Variable Equations

Solve `x + 2x² + x³ = 100`:

```python
x = var('x', domain=ZZ)   # define x as an integer variable
leq = x + 2*x**2 + x**3
sol = solve(leq == 100, x)
print(sol)  # [x == 4]
```

Verify:

```
4 + 2*(4²) + (4³) = 4 + 32 + 64 = 100 ✓
```

```python
leq(x=4)  # returns 100
```

### Higher Degree Polynomial

Solve `x⁴ - 150x³ + 4389x² - 43000x + 131100 = 0`:

```python
x = var('x', domain=ZZ)
leq = x**4 - 150*x**3 + 4389*x**2 - 43000*x + 131100
sol = solve(leq == 0, x)
sol
```

## Linear Equations

### Two Variables

Solve `x + y = 10`:

```python
x = var('x', domain=ZZ)
y = var('y', domain=ZZ)
sol = solve(x + y == 10, (x, y))
sol
# Solution: x = t_0, y = -t_0 + 10 (parameterized)
```

Solve a system `x + y = 10, x = y`:

```python
sol = solve([x + y == 10, x == y], (x, y))
# Solution: x = 5, y = 5
```

### Three Variables

Solve the system:

```
2x + y = 15
x + y + z = 20
3z = 30
```

```python
x = var('x', domain=ZZ)
y = var('y', domain=ZZ)
z = var('z', domain=ZZ)

sol = solve([
    x + x + y == 15,
    z + z + z == 30,
    x + y + z == 20
], (x, y, z))
sol
```

## Matrix Operations

### Matrix Inverse

Find the inverse of:

```
[ 0  2  0  0 ]
[ 3  0  0  0 ]
[ 0  0  5  0 ]
[ 0  0  0  7 ]
```

```python
A = matrix([[0,2,0,0], [3,0,0,0], [0,0,5,0], [0,0,0,7]])
A.inverse()
```

## Finite Fields

### Working in GF(p)

SageMath supports arithmetic in finite fields:

```python
# Create finite field of size 7
Zp = GF(7)

# Arithmetic in GF(7)
a = Zp(5)
b = Zp(4)
print(a + b)   # 2 (because 5 + 4 = 9 ≡ 2 mod 7)
print(a * b)   # 6 (because 5 * 4 = 20 ≡ 6 mod 7)
print(a^(-1))  # 3 (because 5 * 3 = 15 ≡ 1 mod 7)
```

### Elliptic Curve in SageMath

```python
# Define elliptic curve E: y² = x³ + 497x + 1768 over GF(9739)
E = EllipticCurve(GF(9739), [497, 1768])

# Define points
P = E(493, 5564)
Q = E(1539, 4742)
R = E(4403, 5202)

# Compute S = 2P + Q + R
S = 2*P + Q + R
print(S)
```

### RSA in SageMath

```python
# Factor RSA modulus (only works for small n)
n = 35
factor(n)   # 5 * 7

# Extended Euclidean / modular inverse
inverse_mod(3, 7)   # 5 (because 3 * 5 ≡ 1 mod 7)

# Discrete log
p = 997
g = 2
h = power_mod(g, 42, p)  # h = g^42 mod p
discrete_log(h, Mod(g, p))  # returns 42
```

## CTF Workflow

```python
# 1. Define field
F = GF(large_prime)

# 2. Define curve
E = EllipticCurve(F, [a, b])

# 3. Work with points
G = E(gx, gy)   # generator
P = n * G       # scalar multiplication

# 4. Solve DLP (Pohlig-Hellman for small group order)
G.discrete_log(P)
```

## Resources

- [SageMath — Official Documentation](https://doc.sagemath.org/)
- [CryptoHack — Crypto Challenges using SageMath](https://cryptohack.org/)
- [SageMath Online — CoCalc](https://cocalc.com/)
- [A Gentle Introduction to SageMath](https://sagebook.gforge.inria.fr/)
