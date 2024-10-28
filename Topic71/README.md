# ROP Challenge 

Provided with a libc binary and a binary file


Checking the security enabled on the binary during copilation

![Screenshot 2024-10-28 104653](https://github.com/user-attachments/assets/f0326a52-928e-4922-ba15-2bfd016bd329)


This shows that there’s no stack canary, the stack is non-executable, and there’s no PIE enabled, so ASLR won’t be an issue when working with this binary.

Continuing with the binary analysis, I ran it to observe its behavior. It repeatedly prompts for an address, suggesting a while loop and an expected input.

![Screenshot 2024-10-28 105354](https://github.com/user-attachments/assets/01a75f7d-8e0b-44ef-9993-09e671eb9056)


Using GDB, I proceeded to disassemble the main function, as the binary is not stripped.

![Screenshot 2024-10-28 110023](https://github.com/user-attachments/assets/45d999b9-1124-48b8-8fa7-3cbe41c97362)

We can see that the binary sets up a TCP socket and waits for incoming connection requests. This, however, interferes with analyzing the challenge directly. To work around it, I wrote a quick GDB script to allow the function frame to initialize, then bypass the entire socket connection setup.


```
b *main+250

b *main+221

r < ola

set $rip=*main+356
c

```


# Checking Binary Overflow

  supplying a really long input to the binary makes our input overflow the intended buffer assigned for the input into other memory space including rbp and the return address (good thing there is no stack canary). If there is a stack canary we would have had to look a way to leak the canary or bruteforce, since its a fork server


# Overflowing the return pointer

remember ret is 
checking the value of rsp , tells us the offset we need to use to get to return address without segfault
pop rip ; this means the rsp at the time of this instruction will end up in rip ;



# Where to return to ?

Now that we control the return address , we can move anywhere in the binary 


mapping out a plan 

The plan is to get this program to give us a shell access or escalate our privilege (if it runs as any other user with setuid)

how do we do that ? 

with the control we have over the stack , we can patch up a ROP chain that indirectly tells the program what to do by carefully pointing to what next instruction to return to


if i am able to carefully make the program run a syscall and set the argument to this syscall , i can make the program run a shell 



checking for syscall in the binary however turns empty handed, well not expecting it to be that easy but  a man has to try lol


this is not the end is it 


# return to libc 

that doesnt stop our exploit tho, we have a ton of places to return to thanks to libc a binary linked dynamically to our binary here 

since we are provided with the libc binary this binary uses it is important we use it for our exploit , cause this could mean a discrepancy in offset


However we need to know the base address our libc is as all shared library must have PIE hence aslr


# leaking the address of libc 

what better way to leak the libc but to use the puts of our program (plt) to print the puts of libc (got)

read on plt and got here ....


 ### making our program run puts(puts)

  first, we have to find the puts@got and puts@plt

  then we set the argument to the puts@plt to puts@got ;
  setting argument of puts@plt means we have to sets its rdi therefore we have to find the gadget that sets rdi.

  however all the puts@plt functions i saw laid between the socket connections instructions 

  so i used printf@plt 

  pop rdi; ret suits our purpose perfectly. remember we control the stack

  so going over our exploit again

  we control return pointer;
  we point to pop rdi
  we set the stack to the value we want in rdi ; printf@plt 
  once pop rdi returns it gets return address from rsp which we control; where puts@plt awaits
  the instance puts@plt is called , its argument (rdi), will already contain libc puts address , hence leaking our libc address of puts
  then we restart the binary to read in new input for our second payload


building our exploit to this point


```
```


now that we have the address of puts in libc 


we can calculate the base address of the libc based on the static offset of where puts is in the libc binary 





# Second stage 

	calling system("/bin/sh")

after getting the base address of libc, we can successfully move around in libc without bothering about aslr

remember, the first argument is a x86_64 function is rdi , calling a system function means we have to set the pointer to a string for it to execute.

In our case we want to execute shell, we can achive it by looking at the libc binary and looking for any string "/bin/sh" and its address in memory

```
strings -a -t x /lib/x86_64-linux-gnu/libc.so.6 | grep "/bin/sh"
```

after getting this address we can then chain our ROP as follows


offset + pop_rdi + value_to_pop_into_rdi ("/bin/sh") + address_of_system 



# SHELL !
