---
title: "CTF (Capture the Flag)"
topic: "ctf"
tags: [ctf, pwn, web, crypto, forensics, reverse-engineering, competition]
difficulty: beginner
day: 31
layout: default
parent: Topics
nav_order: 31
---

# CTF (Capture the Flag)

## What You Will Learn
- What a CTF competition is and how it works
- The main categories of CTF challenges
- How to approach CTF problems for the first time
- Useful tools and resources for getting started

## What Is It?

A **Capture the Flag (CTF)** is a cybersecurity competition where participants solve security challenges to find hidden strings called **flags**. A flag usually looks like `flag{some_text_here}` or a custom format like `HTB{...}` or `picoCTF{...}`.

CTFs are one of the best ways to learn hacking skills in a legal and structured environment. You solve puzzles that teach you real offensive and defensive techniques.

## Why It Matters

CTFs build practical skills that you cannot get from textbooks alone. They expose you to:
- Real vulnerability classes (buffer overflows, SQL injection, XSS)
- Reverse engineering and binary analysis
- Cryptographic attacks
- Network analysis

Many professional security researchers and penetration testers started with CTFs. They are also a great way to build a portfolio.

## Key Concepts

### CTF Categories

| Category | Description |
|----------|-------------|
| **Web** | Find vulnerabilities in web applications — XSS, SQLi, SSRF, IDOR |
| **Pwn / Binary Exploitation** | Exploit memory corruption bugs in binaries — buffer overflow, ROP, heap exploits |
| **Reverse Engineering** | Analyze binaries without source code to find flags |
| **Cryptography** | Break weak encryption schemes or flawed implementations |
| **Forensics** | Analyze files, memory dumps, network captures |
| **Miscellaneous** | Steganography, OSINT, programming challenges |

### Flag Format

Most CTFs use a standard flag format:

```
flag{this_is_the_flag}
CTF{some_value}
picoCTF{abc123}
HTB{secret_value}
```

### CTF Formats

- **Jeopardy**: Individual challenges worth points. Solve as many as you can.
- **Attack/Defense**: Teams run services and attack each other's infrastructure.
- **King of the Hill**: Maintain access to a server longer than other teams.

## Hands-On

### Getting Started

```bash
# Install essential CTF tools
sudo apt install gdb pwndbg binutils python3 nmap netcat

# Install pwntools (Python library for exploit development)
pip install pwntools

# Install radare2 for binary analysis
sudo apt install radare2
```

### A Simple Pwn Workflow

```python
from pwn import *

# Connect to remote challenge
p = remote('challenge.ctf.com', 1337)

# Or run locally
p = process('./vuln_binary')

# Send payload
payload = b"A" * 64 + p64(0xdeadbeef)
p.sendline(payload)

# Get response
p.interactive()
```

### Useful Commands for CTF

```bash
# Look for strings in a binary
strings binary | grep flag

# Check binary protections
checksec binary

# Decode base64
echo "dGhpc2lzYWZsYWc=" | base64 -d

# Hex decode
echo "666c6167" | xxd -r -p
```

## Resources

- [picoCTF — Beginner-friendly CTF platform](https://picoctf.org/)
- [Hack The Box — CTF-style machines and challenges](https://www.hackthebox.com/)
- [CTFtime — CTF calendar and writeup archive](https://ctftime.org/)
- [pwn.college — Free pwn/CTF learning platform](https://pwn.college/)
- [Trail of Bits CTF Guide](https://trailofbits.github.io/ctf/)
