import requests

def get_cipher():
    url = "http://aes.cryptohack.org/bean_counter/encrypt/"
    rsp = requests.get(url)
    return rsp.json()['encrypted']

def xor(var, key, plain):
    return bytes(a ^ b ^ c for a, b, c in zip(var, key, plain))

png_hdr = bytes([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a, 0x00, 0x00, 0x00, 0x0d, 0x49, 0x48, 0x44, 0x52])
cipher = bytes.fromhex(get_cipher())

print(png_hdr)

# take first 16 bytes and xor with next 16 bytes (T canceled ) remains header xor plain2 
# header xor plain2  xor png_hdr to gain plain2



# sec xor third

chunk = 16

with open("flag.png", 'wb') as f:
    f.write(png_hdr)
    plain = xor(cipher[:16], cipher[16:32], png_hdr)
    for i in range(16, len(cipher), chunk):
        f.write(plain)
        plain = xor(cipher[i:i+chunk], plain, cipher[i+chunk:i+chunk+chunk])
    

