#!/usr/bin/env python3
import hashlib
from Crypto.Util.number import bytes_to_long
from ecdsa.ecdsa import Public_key, Private_key, Signature, generator_192

# Curve setup
G = generator_192
n = G.order()

def sha1_bytes(m: bytes) -> bytes:
    h = hashlib.sha1()
    h.update(m)
    return h.digest()

def recover_private(msg, r_hex, s_hex):
    """
    Recover the private key d from one signature where k is <= 59.
    msg is like "Current time is 8:42".
    """
    # Parse inputs
    r = int(r_hex, 16)
    s = int(s_hex, 16)

    # Compute hash of the message (same as the server does)
    h = bytes_to_long(sha1_bytes(msg.encode()))

    # Extract the seconds from the msg "M:S"
    M, S = map(int, msg.split()[-1].split(":"))

    rinv = pow(r, -1, n)  # modular inverse of r

    for k in range(1, S):  # k was chosen from 1..S-1
        d = (s * k - h) * rinv % n

        # Build pubkey from candidate d
        Q = G * d
        pub = Public_key(G, Q)

        sig = Signature(r, s)
        if pub.verifies(h, sig):   # check if this d is correct
            return d, k

    raise Exception("Failed: maybe need another signature")


# Example usage with the leaked JSON from the challenge
if __name__ == "__main__":
    # Example values you’d get from the server:
    json_message = {"msg": "Current time is 8:26", "r": "0xfd41ce1bce22d0f6de1c3ec75dd185863c4963ca1b91a56a", "s": "0x981639bb87df5f027920a09f841304fde44c6d3f43953273"}
    
    msg  = json_message['msg']
    r_hex = json_message['r']
    s_hex = json_message['s']

    d, k = recover_private(msg, r_hex, s_hex)
    print("[+] Recovered private key d =", hex(d))
    print(k)

    # Now you can sign "unlock"
    
    pub = Public_key(G, G * d)
    priv = Private_key(pub, d)
    h_unlock = bytes_to_long(sha1_bytes(b"unlock"))
    sig = priv.sign(h_unlock, k)   # pick any small k != 0
    print("[+] Forged signature for 'unlock':")
    print("r =", hex(sig.r))
    print("s =", hex(sig.s))
