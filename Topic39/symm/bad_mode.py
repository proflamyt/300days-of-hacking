ciphertext = "a6d86c3edab28464aebdbd6014df05ac93c5c0daa511c392caa07b69b83a0b841566266adc682707e4e16bc657c3bcca"

iv = ciphertext[:32]

cipher = ciphertext[32:]

plain = "c5aa154eaeddff57cddfe25561bc6e99ccf1b6ea94759ca3fdff5a48991b2af9"


def encrypt(var, key):
    return bytes(a ^ b for a, b in zip(var, key))

def main():
    chunk = 32
    print(encrypt(bytes.fromhex(iv), bytes.fromhex(plain[:32])), end='')
    for i in range(0, len(cipher), 32):
        print(encrypt(bytes.fromhex(cipher[i:i+chunk]), bytes.fromhex(plain[i+32:i+chunk+32])))




if __name__ == '__main__':
    main()