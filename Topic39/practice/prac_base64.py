import base64

hex_format = '72bca9b68fc16ac7beeb8f849dca1d8a783e8acf9679bf9269f7bf'
# hex to bytes
byte_format = bytes.fromhex(hex_format)


print(base64.b64encode(byte_format).decode())