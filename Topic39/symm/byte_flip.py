# Byte Flipping attack


ciphertext = "3fa41d59f330412b3cc0e3cf52acf4e56f06b7499d03daf169423184734f3ede83317e9f2dadf8cf419ff23fdc780fa9"

iv = ciphertext[:32]

def encrypt(var, key):
    return bytes(a ^ b for a, b in zip(var, key))



def main():
    after_decryption = encrypt(bytes.fromhex(iv), b'admin=False;expir')
    print(after_decryption.hex())
    # we want T xor Iv == admin=True
    new_iv = encrypt(bytes.fromhex(after_decryption.hex()), b'admin=True;expir')
    print(new_iv.hex())
    print(ciphertext[32:])

    
main()

