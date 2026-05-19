---
title: "GDB (GNU Debugger)"
topic: "gdb"
tags: [gdb, debugging, binary-exploitation, assembly, linux, reverse-engineering]
difficulty: intermediate
day: 55
layout: default
parent: Topics
nav_order: 55
---

# GDB (GNU Debugger)

## What You Will Learn
- How to navigate and debug binaries with GDB
- How to inspect registers, memory, and the stack
- How to set breakpoints and step through code
- Advanced GDB tricks for exploit development

## What Is It?

**GDB** (GNU Debugger) is the standard debugger for Linux programs. It lets you run a program step-by-step, inspect memory, modify registers, and understand exactly what a program is doing. It is the most important tool for binary exploitation and reverse engineering on Linux.

## Setup

```bash
# Set Intel syntax (easier to read than AT&T)
echo "set disassembly-flavor intel" >> ~/.gdbinit

# Install pwndbg or peda for better output
git clone https://github.com/pwndbg/pwndbg
cd pwndbg && ./setup.sh
```

## Core Commands

```bash
# Start GDB with a binary
gdb ./binary

# Start and stop at the first instruction
starti

# Run the program normally (no breakpoints)
run
r

# Continue execution after a breakpoint
continue
c
```

## Breakpoints

```bash
# Break at a function name
break main
b main

# Break at an address
b *0x401234

# Break at function + offset
b *main+64

# List breakpoints
info break

# Delete a breakpoint
delete 1

# Disable / enable a breakpoint
disable 1
enable 1
```

## Stepping

```bash
# Step one instruction (follows calls INTO functions)
si

# Step one instruction (steps OVER function calls)
ni

# Next source line (source-level step over)
next
n

# Step into source line
step
s

# Finish current function and return to caller
finish
```

## Registers and Memory

```bash
# Display all registers
info registers
i r

# Display specific register in hex
p/x $rdi

# Display next 8 instructions from RIP
display/8i $rip

# Display 4 quad-words (8 bytes each) from RSP
display/4gx $rsp

# Examine memory
# x/<count><format> <address>
x/16xb $rsp       # 16 bytes as hex
x/4gx $rsp        # 4 quad-words
x/10i $rip        # 10 instructions from RIP
x/s $rdi          # string at rdi
```

## Process Information

```bash
# Memory map of the process
info proc map

# Stack frame info
info frame

# List source files (if debug info available)
info sources
```

## Disassembly

```bash
# Disassemble a function
disas main
disassemble main

# Disassemble at current instruction
disas $rip
```

## Advanced: TLS and File Structures

```bash
# Access the Thread Control Block (TLS struct)
ptype struct tcbhead_t
set $tcb = (struct tcbhead_t *)$fs_base
p *$tcb

# Get offset of _IO_read_ptr inside FILE struct
p &((struct _IO_FILE *)0)->_IO_read_ptr

# Cast a pointer to a FILE struct
p *(struct _IO_FILE_plus *) fp
```

## Analyzing setuid Programs

```bash
# 1. Copy program to a writable location
cp /usr/bin/suid_binary /tmp/

# 2. Set base address for PIE binaries in ~/.gdbinit
nano ~/.gdbinit
# add: set $BASE = 0x0000555555554000
```

## GDB Scripting

```bash
# Run GDB with a script file
gdb -x script.gdb ./binary

# Script contents example:
# b *main+100
# r < input.txt
# set $rip=*main+200
# c
```

## Resources

- [pwndbg — Enhanced GDB for Exploit Dev](https://github.com/pwndbg/pwndbg)
- [GDB Documentation](https://sourceware.org/gdb/current/onlinedocs/gdb/)
- [pwn.college — Debugging](https://pwn.college/)
- [TryHackMe — Intro to GDB](https://tryhackme.com/)
- [GDB Cheat Sheet](https://darkdust.net/files/GDB%20Cheat%20Sheet.pdf)
