
hex_str = '73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d'

# Convert the hex string to bytes
byte_str = bytes.fromhex(hex_str)
for i in range(255):
# XOR each byte with 17 and convert back to bytes
    result_bytes = bytes([b ^ i for b in byte_str])

    if b'crypto' in result_bytes:
        print(result_bytes.decode())

