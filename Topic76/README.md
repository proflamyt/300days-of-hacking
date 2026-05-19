---
title: "WinDbg"
topic: "windbg"
tags: [windbg, windows, debugging, reverse-engineering, kernel, malware-analysis]
difficulty: advanced
day: 76
layout: default
parent: Topics
nav_order: 76
---

# WinDbg

## What You Will Learn
- How to navigate and debug programs with WinDbg
- How to set breakpoints, inspect registers, and examine memory
- How to step through code and analyze function calls
- How to use WinDbg for kernel and malware analysis

## What Is It?

**WinDbg** is Microsoft's official debugger for Windows. It supports both user-mode and kernel-mode debugging. It is the standard tool for Windows crash dump analysis, malware analysis, and kernel debugging.

Unlike GDB, WinDbg uses a different syntax and has a unique command structure.

## Basic Navigation

```
g                     ; go (continue execution)
```

## Listing Modules

```
lm                    ; list all loaded modules
```

## Symbols and Addresses

```
x module!function     ; get address of a function in a module
x ntdll!NtCreateFile  ; example: address of NtCreateFile in ntdll
```

## Call Stack

```
k                     ; display call stack (backtrace)
kv                    ; verbose call stack with parameters
kb                    ; call stack with first 3 parameters
```

## Disassembly

```
u $entry              ; unassemble from entry point
uf module!function    ; unassemble entire function
u @rip                ; unassemble from current instruction pointer
```

## Breakpoints

```
bp $exentry           ; break at entry point
bp 0x00401000         ; break at address
bu module!function    ; breakpoint on unresolved function (set when loaded)
bd <num>              ; disable breakpoint number
be <num>              ; enable breakpoint number
bl                    ; list all breakpoints
```

## Stepping

```
t                     ; trace — step into one instruction
p                     ; step over one instruction
p 5                   ; step over 5 instructions
gu                    ; go up — run until current function returns
tc                    ; trace until next call instruction
```

## Registers

```
r                     ; display all registers
r rax = 0xdeadbeef    ; set rax to a value
r ax = 0xf00d, rbx = 0xdeadfacebeefd00d, bl = 0x0f
```

## Memory Examination

```
# Display memory at address
db <address> L<count>   ; display <count> bytes as hex+ASCII
dd <address> L<count>   ; display <count> doublewords (4 bytes) as hex
dq <address> L<count>   ; display <count> quadwords (8 bytes) as hex
da <address>            ; display as ASCII string until null terminator

# Examples
db 0x00401000 L10       ; 10 bytes from 0x00401000
dq @rsp L8              ; 8 quadwords from stack pointer
da @rdi                 ; ASCII string at rdi
```

## Memory Modification

```
ed rsp 0xdeadbeef       ; write doubleword to rsp
eq rsp 0xdeadfacebeef   ; write quadword to rsp
```

## Expression Evaluation

```
? a - b                 ; evaluate expression a minus b
? 0x1000 + 0x100        ; calculate hex arithmetic
```

## Reload Symbols

```
.reload /f              ; force reload all symbols
```

## Dump from RSP

```
dq @rsp                 ; dump quadwords from stack pointer
```

## Example: Analyzing a Windows Binary

```
# 1. Load the binary
windbg -o "C:\target.exe"

# 2. Set symbol path
.sympath SRV*C:\symbols*https://msdl.microsoft.com/download/symbols

# 3. Break at entry
bp $exentry
g

# 4. See where we are
k
u @rip

# 5. Find a specific function
x target!main

# 6. Break at main
bp target!main
g
```

## Kernel Debugging

WinDbg is used for kernel debugging by connecting a debugger machine to the target over a serial cable, network, or virtual machine serial port.

```
# On target machine
bcdedit /debug on
bcdedit /dbgsettings net hostip:192.168.1.100 port:50000 key:1.1.1.1

# On debugger machine
windbg -k net:port=50000,key=1.1.1.1
```

## Resources

- [OpenSecurityTraining2 — WinDbg Course](https://apps.p.ost2.fyi/learning/course/course-v1:OpenSecurityTraining2+Dbg1011_WinDbg1+2021_v1)
- [Microsoft WinDbg Documentation](https://learn.microsoft.com/en-us/windows-hardware/drivers/debugger/)
- [TryHackMe — Windows Debugging](https://tryhackme.com/)
- [WinDbg Preview (App Store)](https://apps.microsoft.com/detail/windbg-preview/9PGJGD53TN86)
