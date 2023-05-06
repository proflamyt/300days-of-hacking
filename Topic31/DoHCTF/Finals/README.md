# CyberStarters Finals

I was priviledge to be one of the participants in DoH CTF finals, I must say it was a really great game, even though my team came 5th , haha ... It was really an eye opener and challenge to be better at our crafts. 

As usual here are some of the challenges with the least solves.



### Guess

Guess is a prompt challenge that requires we guess a number between one and 1 billion

> Guess an integer btw 1 and 1 billion

Bruteforcing a number between 1 and a billion is a small feat for a computer, it even gets easier when the said computer discloses more info about the number you are to get. The game tells us if the number is higher that what we guessed or lower, using this information i decided to use binary search , unfortunately during the CTF, i closed the TCP connection per guess and worndered why i couldn't get the guess right , apparently the backend application is also picking a random number between one and 1 billion, therefore restarting the game will give you a diffrent number entirely. T 

My Approach:

i opened a tcp connection to the given Host and post, mimicked the manual way i would have typed in and guessed the numbers , 

1. First I would have connected using nc HOST POST (so i opened a tcp socket stream) # socket.socket(socket.AF_INET, socket.SOCK_STREAM)
2. Next I would have gotten an Input "Guess an integer btw 1 and 1 billion"
3. Then comes in the bruteforcing, here instead of going through a billion numbers, binary search was the most efficient since we an information about the said number was disclosed (if it is higher that our current guess or lower)


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
