# Cryptography

ASCII : A 7 bit encoding number used to represent characters in the alphabeth they are represented by integers betweeen  0-127.



 In Python, the chr() function can be used to convert an "ASCII ordinal number" to a character, and the ord() function can be used to convert character to Ascii number.

 Hexadecimal can be used in such a way to represent ASCII strings. First each letter is converted to an ordinal number according to the ASCII table . Then the decimal numbers are converted to base-16 numbers, otherwise known as hexadecimal. The numbers can be combined together, into one long hex string.

Using bytes.fromhex function , each hex would be converted to its equivalent decimal number , then to it's byte representative (8 bits) which can be turned into ascii.


Base64 encoding can also be used to represent bytes as an ASCII string, in a format that can be easily transmitted over networks and stored in text-based formats. One character of a Base64 string encodes 6 bits

## TrapDoor Function
trapdoor functions allow a client to keep data secret by performing a mathematical operation which is computationally easy to do, but currently understood to be very expensive to undo.

XOR is a bitwise operator which returns 0 if the bits are the same, and 1 otherwise. 

XOR PROPERTIES (⊕ == xor() == ^)

```
Commutative: A ⊕ B = B ⊕ A
Associative: A ⊕ (B ⊕ C) = (A ⊕ B) ⊕ C
Identity: A ⊕ 0 = A
Self-Inverse: A ⊕ A = 0

```

### Modular Arithmetic

*The quotient remainder theorem*:
Given any integer A, and a positive integer B, there exist unique integers Q and R such that

```
A = B * Q + R where 0 ≤ R < B

Example:

9 = 4 * 2 + 1

therefore 9 % 4 = 1 , since 1 is the remainder (R)

```

*Modular Addition*

```
(A + B) mod C = (A mod C + B mod C) mod C
```

*Modular subtraction*

```
(A - B) mod C = (A mod C - B mod C) mod C
```

*Modular multiplication*

```
(A * B) mod C = (A mod C * B mod C) mod C
```

*Modular exponential*

```
A^B mod C = ( (A mod C)^B ) mod C
```

*GCD*: The Greatest Common Divisor (GCD), sometimes known as the highest common factor, is the largest number which divides two positive integers 
Euclidean algorithm, is an efficient method for computing the greatest common divisor (GCD) of two integers (numbers). The Euclidean algorithm is based on the principle that the greatest common divisor of two numbers does not change if the larger number is replaced by its difference with the smaller number. For example, 21 is the GCD of 252 and 105 (as 252 = 21 × 12 and 105 = 21 × 5), and the same number 21 is also the GCD of 105 and 252 − 105 = 147. Since this replacement reduces the larger of the two numbers, repeating this process gives successively smaller pairs of numbers until the two numbers become equal. When that occurs, they are the GCD of the original two numbers.

Using this method to find the gcd(252, 105)

> replacing the larger number with the diffrence with its smaller conterpart (252 - 105)

```
147, 105
42, 105
63, 42
21, 42
21, 21 ==> gcd

```

A more efficient version of the algorithm shortcuts these steps, instead replacing the larger of the two numbers by its remainder when divided by the smaller of the two (with this version, the algorithm stops when reaching a zero remainder).

```
42, 105
21, 42
42, 21 ==> gcd
```

## Etended Euclidean 
The extended Euclidean algorithm is an algorithm to compute integers p, q

such that px + qy = gcd(a,b)






#  LSB ORACLE ATTACK





### ECC 


### 🧮 Elliptic Curve Point Addition Example

We are given the elliptic curve:

\[
E: Y^2 = X^3 + 497X + 1768 \mod 9739
\]

Points:

- \( P = (493, 5564) \)
- \( Q = (1539, 4742) \)
- \( R = (4403, 5202) \)

We are to compute:

\[
S = P + P + Q + R = 2P + Q + R
\]

---

```
# Define the field and curve
p = 9739
a = 497
b = 1768

# Elliptic curve point addition
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

# Define the points
P = (493, 5564)
Q = (1539, 4742)
R = (4403, 5202)

# Compute S = P + P + Q + R
S1 = point_add(P, P)      # 2P
S2 = point_add(S1, Q)     # 2P + Q
S  = point_add(S2, R)     # 2P + Q + R

print("S =", S)

```




refrence: https://en.wikipedia.org/wiki/Euclidean_algorithm
https://brilliantorg-infra-prod.brilliant.org/wiki/extended-euclidean-algorithm/
https://www.khanacademy.org/computing/computer-science/cryptography/modarithmetic/a/what-is-modular-arithmetic
