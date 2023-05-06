# DoHCTF Finals 





```python

import sys
import socket

HOST = '0.cloud.chals.io'
PORT = 30963
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(s.recv(1024) )





def make_a_guess():
    left = 0
    right = 1_000_000_000
    while True:
        
        mid = (left + right) // 2
        s.sendall(str(mid).encode()) 
        print(s.recv(1024)) # number back
        s.sendall(b'\n')
        data = s.recv(1024) # higer
        print(f"{data=}")
        if  'Higher' in data.decode() :
            left = mid 
            continue
        elif  'Lower' in data.decode() :
            right = mid
        else :
            return data
        
        


if __name__ == '__main__':
    print(f'[*] Starting Binary Sort BruteForcing ...')

    print(make_a_guess())
    
    print('[*] Done! .')

```





