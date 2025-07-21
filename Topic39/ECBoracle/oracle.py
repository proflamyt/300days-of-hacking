import pwn
import base64
from Crypto.Util.Padding import pad
import string


initial = b"a" * 7

process = pwn.process("/challenge/run")
process.readuntil("plaintext prefix (b64): ")
process.sendline(base64.b64encode(initial).decode())
process.readuntil("plaintext prefix (b64): ")


output = ""
all_strings = string.ascii_letters + string.digits + '{.-_}]\n' 


def get_prob(number):
    return b'a' * number

def character_pad(characters):
    return pad(characters.encode(), 16)


def send_payload(payload: str, last: bool):

    process.sendline(payload)

    process.readuntil("ciphertext (hex): ")

    note = process.readline().decode().strip()

    ecbs = note.split(" ")

    rev = 4 - len(ecbs)

    if last:
        last =  ecbs[rev]
    else :
        last =  note.split(" ")[0]


    process.readuntil("plaintext prefix (b64): ")

    return last




for number in range(8, 200):
    prod = get_prob(number)
    last_block = send_payload(payload=base64.b64encode(prod).decode(), last=True)
    
    for i in all_strings:
        str_topad = f"{i}{output}"
        prod = character_pad(str_topad)
        first_block = send_payload(payload=base64.b64encode(prod).decode(), last=False)
        if first_block == last_block:
            output = i + output
            print("=============", output)
            break



