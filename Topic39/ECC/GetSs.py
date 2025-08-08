def inverse_mod(k, p):
    return pow(k, -1, p)

def point_add(P, Q, a, p):
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
        m = ((3 * x1**2 + a) * inverse_mod(2 * y1, p)) % p

    x3 = (m**2 - x1 - x2) % p
    y3 = (m * (x1 - x3) - y1) % p
    return (x3, y3)

def scalar_mult(k, P, a, p):
    Q = "O"
    N = P

    for bit in bin(k)[2:]:
        Q = point_add(Q, Q, a, p)  # double
        if bit == '1':
            Q = point_add(Q, N, a, p)  # add

    return Q



p = 9739
a = 497
P = (4726, 6287) # possible first p
P2 = (4726, 3452)
k = 6534



result = scalar_mult(k, P, a, p)
print(f"{k}P =", result)

result = scalar_mult(k, P2, a, p)
print(f"{k}P =", result)
# 7863P = (9467, 2742)
