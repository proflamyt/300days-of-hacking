def extended_gcd(a, b):
    if b == 0:
        return a, 1, 0
    else:
        gcd, x, y = extended_gcd(b, a % b)
        return gcd, y, x - (a // b) * y

def modular_inverse(e, phi):
    gcd, x, _ = extended_gcd(e, phi)
    if gcd == 1:
        return x % phi
    else:
        raise ValueError("Modular inverse does not exist.")

# Given values
p = 857504083339712752489993810777
q = 1029224947942998075080348647219
e = 65537

N = p * q
phi = (p - 1) * (q - 1)
d = modular_inverse(e, phi)

private_key = (N, d)

print("Private key:", private_key)
