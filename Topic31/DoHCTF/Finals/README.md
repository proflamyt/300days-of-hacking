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





# Segs

Got a binary File name segs 

My Approach:

first my enumeration, i had to know what type of file it is . so i used the file command

```
file segs
```
The output says it is an ELF 64 bit binary  and most importantly stripped (not good , for me at least lol), this means the file has had its metadata stripped , we wont be able to get stuff like meaningful variable names etc. Simple put Dymanically linked means, some of its libraries are expected to be on the executing machine , if it were to be statically link , it would have packed all its library in the binary, the downside is bigger size, stiffer updates, but it would execute without dependency. 

```
segs: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=251069e7c121cc083461edb65f5f603d6dafd923, for GNU/Linux 3.2.0, stripped

```

so, running strings on the binary will provide little info (i did it anyway) , so i decomipled the code using ghidra, just has i expected , i had difficulty locating the entry point, usually the main or _start() , but i did track a function that seems to be executing the main logic on ghidra


```C

undefined8 FUN_0010130e(void)

{
  int local_c;
  
  printf("Flag: ");
  DAT_00104090 = 0x10138b;
  for (local_c = 0; local_c < 0xe; local_c = local_c + 1) {
    __isoc99_scanf(&DAT_0010200b,&DAT_00104088);
    DAT_00104088 = (long *)((ulong)DAT_00104088 ^ *DAT_00104088 + 0x1337U);
  }
  if (DAT_00104088 == (long *)0xdeadbeef) {
    puts("Good");
  }
  else {
    puts("Bad");
  }
  return 0;
}

```


To make it more readable to me to make sense of , i renamed some of the variables and function name, converted the hexadecimals to decimals and so i ended up with:


```C

int main(void)

{
  int i;
  
  printf("Flag: ");
  DAT_00104090 = 1053579;
  for (i = 0; i < 14; i = i + 1) {
    scanf(&DAT_0010200b,&encoded_input);
    encoded_input = (long *)((ulong)encoded_input ^ *encoded_input + 0x1337U);
  }
  if (encoded_input == (long *)0xdeadbeef) {
    puts("Good");
  }
  else {
    puts("Bad");
  }
  return 0;
}

```
So,  my deduction is, the program is taking an input from us 14 times, performing an encryption on this input and comparing the result with what is inside the address "0xdeadbeef"

now question is what is inside this address and how does this program behave,so lets run dynamic analysis with gdb


first i ran segs and gave it an input 14 time, ofcourse it printed bad, the i gave it a bunch of As to test its input and it returned 'Bad'


```
gdb -q segs
```






