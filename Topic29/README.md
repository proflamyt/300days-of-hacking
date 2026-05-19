---
title: "Reverse Engineering"
topic: "reverse-engineering"
tags: [reverse-engineering, assembly, ghidra, gdb, elf, static-analysis, dynamic-analysis]
difficulty: advanced
day: 29
layout: default
parent: Topics
nav_order: 29
---

# Reverse Engineering

## What You Will Learn
- What reverse engineering is and what its goals are
- How x86 assembly relates to compiled programs
- What ELF binaries are and how to inspect them
- The difference between static and dynamic analysis
- What tools are used for reverse engineering

## What Is It?

The goal of reverse engineering is understanding **WHAT** a program does and **HOW** it does it — without access to the source code.

Security researchers reverse engineer malware to understand its capabilities. CTF players reverse engineer challenge binaries to find hidden flags. Vulnerability researchers reverse engineer software to find exploitable bugs.

Reference: https://0xinfection.github.io/reversing

## Why It Matters

Reverse engineering is at the core of:
- Malware analysis
- Vulnerability research
- CTF competitions
- Software interoperability

## Key Concepts

### x86 Basic Architecture

A computer application is simply a table of machine instructions stored in memory. The basic architecture of the computer comprises the CPU, bus, memory, and basic I/O.

The CPU (Central Processing Unit) executes the computer program. The bus moves data between the memory and CPU for processing. The memory stores information to be processed. The CPU stores data internally using its **registers** and uses **flags** to indicate events during execution.

In a 32-bit Intel processor, there are several types of registers:

1. **General-purpose registers**: 8 registers, each 32 bits wide. Used to hold data and addresses during program execution.
2. **Segment registers**: 6 registers, each 16 bits wide. Hold segment selectors pointing to different segments of memory.
3. **Control registers**: Include the program counter (PC), flags register, and instruction pointer (IP).
4. **Debug registers**: Used by the processor to assist with debugging.

A 32-bit Intel processor has around 20 registers in total.

### Memory Dereferencing

```assembly
mov rax, [rdx]       ; Move the value AT the address in rdx into rax
mov [rax], rdx       ; Move the value of rdx into the memory address stored in rax
```

```assembly
; If RBP = 0x7FFF0000 and local_18 is at offset -0x18:
MOV RAX, qword ptr [RBP + local_18]
; = MOV RAX, qword ptr [0x7FFF0000 - 0x18]
; = MOV RAX, qword ptr [0x7FFFE7E8]
; Fetches 8 bytes from that address into RAX
```

## ELF Binary

The **ELF (Executable and Linkable Format)** is the common standard file format for executable files on Unix/Linux systems.

An ELF file consists of two main sections:

1. **ELF header**: 32 bytes long, starting with 4 unique bytes: `0x7F` followed by `0x45`, `0x4C`, `0x46` (which spells "ELF").
2. **File data**: Program headers, section headers, and the actual code/data.

![ELF Header](https://github.com/proflamyt/300days-of-hacking/assets/53262578/1499d412-d85f-4f68-a0b5-1e79e1c77320)

![ELF Sections](https://github.com/proflamyt/300days-of-hacking/assets/53262578/71438ea0-ad14-480b-bc49-8d3ce19e8b7e)

The `.interp` section of the ELF executable contains the location of its required loader — this tells the operating system which loader to use to execute the binary.

![.interp section](https://github.com/proflamyt/300days-of-hacking/assets/53262578/a45003d9-8094-4662-85b9-f51b7f8ed2fd)

### Check Libraries Required by an ELF Binary

```bash
ldd <elf_binary>
```

`ld.so` is the dynamic linker/loader that comes with glibc. It loads shared libraries for an ELF executable during execution so the process has access to external functions.

## Tools

- **GDB**: GNU debugger — for dynamic analysis of Linux binaries.
- **Ghidra**: Open-source reverse engineering suite by the NSA. Excellent decompiler.
- **IDA Pro**: Industry-standard disassembler and decompiler.
- **Radare2**: Open-source framework for reverse engineering and binary analysis.

## Static Analysis

Static analysis examines a binary without executing it.

```bash
# Decompile and view binary online
# dogbolt.org — compare multiple decompiler outputs

# View strings in a binary
strings <binary>

# Check for symbols
nm <binary>

# Disassemble
objdump -d <binary>
```

Unpacking the app and checking its content is the first step in static analysis.

## Dynamic Analysis

Dynamic analysis examines a binary while it is running — observing its behavior at runtime.

```bash
# Attach GDB to a running process
gdb -p <PID>

# Run binary under GDB
gdb ./<binary>

# Set a breakpoint at main
(gdb) break main
(gdb) run
(gdb) disassemble main
```

## IDA Pro Tips

**Define a custom struct:**

```
Shift+F1
→ Local Types
→ Insert

struct yarn_struct {
    char buf[256];
    char reg1;
    char reg2;
    char reg3;
    char reg4;
    char reg5;
}
```

**Convert to signed:**

```python
hex((-0x72) & (2**64 - 1))
```

## Resources

- [0xinfection.github.io — Reversing](https://0xinfection.github.io/reversing/pages/)
- [Ghidra](https://ghidra-sre.org/)
- [dogbolt.org — Online Decompiler Explorer](https://dogbolt.org/)
- [TryHackMe — Reverse Engineering](https://tryhackme.com/room/reverseengineering)
- [pwn.college — Reverse Engineering Module](https://pwn.college/)
