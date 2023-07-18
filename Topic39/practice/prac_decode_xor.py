import sys


KEY1 = 0xa6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313
KEY2xKEY1 = 0x37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e
KEY2xKEY3 = 0xc1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1
FLAGxKEY1xKEY3xKEY2 = 0x04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf


#  key2 = key1 ^ key2 ^ key 1 ; since key1 ^ key1 = 0 therefore  key2 ^ 0 = Key2
#  key3 = key3 ^ key2 ^ key 2 ; since key2 ^ key2 = 0 therefore  key3 ^ 0 = Key3



Key2 = int(hex(KEY1 ^ KEY2xKEY1), 16)

Key3 = int(hex(Key2 ^ KEY2xKEY3), 16)


Flag = hex(FLAGxKEY1xKEY3xKEY2 ^ KEY1 ^ Key2 ^ Key3)[2:]
    
print(bytes.fromhex(Flag).decode())