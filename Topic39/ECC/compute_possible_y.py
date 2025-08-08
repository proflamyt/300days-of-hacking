# Elliptic curve parameters
p = 9739
a = 497
b = 1768
x = 4726

# Compute RHS of the curve equation
rhs = (x**3 + a * x + b) % p

# Check if a square root exists using Legendre symbol
def legendre_symbol(n, p):
    return pow(n, (p - 1) // 2, p)

# Compute square root modulo p (only valid for p ≡ 3 mod 4)
def sqrt_mod_p(n, p):
    if legendre_symbol(n, p) != 1:
        return None  # No square root exists
    # Only works if p ≡ 3 mod 4
    y = pow(n, (p + 1) // 4, p)
    return y, p - y  # Two square roots: y and -y mod p

# Compute y
y_roots = sqrt_mod_p(rhs, p)

print(f"Possible y values for x = {x}: {y_roots}")
