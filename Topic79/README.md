---
title: "ARM64 Assembly"
topic: "arm64-assembly"
tags: [arm64, aarch64, assembly, apple-silicon, macos, ios, registers, syscalls, pac]
difficulty: advanced
day: 79
layout: default
parent: Topics
nav_order: 79
---

# ARM64 Assembly

## What You Will Learn
- How ARM64 registers work (X and W variants)
- Core instructions: mov, add, mul, ldr/str, ldp/stp, branches
- How function prologue and epilogue work on ARM64
- How syscalls work on Linux and macOS ARM64
- What PAC (Pointer Authentication Codes) is

## What Is It?

ARM64 (also called AArch64) is the 64-bit ARM instruction set. It is used on Apple Silicon (M1/M2/M3), iOS devices, Android devices, and modern Linux servers. Understanding ARM64 assembly is essential for iOS/macOS security research and embedded exploitation.

## Registers

ARM64 registers are either 64-bit **X registers** (X0..X30) or 32-bit **W registers** (W0..W30). W registers are the lower 32 bits of the corresponding X register.

| Register | Purpose |
|----------|---------|
| X0–X7 | Arguments and return values |
| X8 | Indirect result register |
| X9–X15 | Caller-saved (temporary) |
| X19–X28 | Callee-saved |
| X29 (FP) | Frame pointer |
| X30 (LR) | Link register (return address) |
| SP | Stack pointer |
| PC | Program counter (not directly accessible) |

### Equivalent x86-64 Registers

```
RIP → PC
RAX → X0 (first integer/return arg)
RBX → X19 (callee-saved)
RCX → X1
RDX → X2
RSP → SP (stack pointer)
RBP → X29 (frame pointer)
LR (return address) → X30 (link register)
```

## Instructions

### mov — Load Immediate

```asm
mov x1, #0xbeef
movk x1, #0xdead, lsl 16   ; load upper 16 bits
; result: x1 = 0xdeadbeef
```

### Arithmetic

```asm
add X0, X1, X2       ; X0 = X1 + X2
mul X1, X0, X1       ; X1 = X0 * X1
udiv X2, X0, X1      ; X2 = X0 / X1 (unsigned)
madd X3, X0, X1, X2  ; X3 = X2 + (X0 * X1)
msub X3, X0, X1, X2  ; X3 = X2 - (X0 * X1)
```

### Modulus

ARM64 has no modulus instruction. Compute it manually:

```
5 / 2 = 2 remainder 1
remainder = dividend - (quotient * divisor)
= 5 - (2 * 2) = 1
```

```asm
udiv X2, X0, X1        ; X2 = X0 / X1 (quotient)
msub X3, X2, X1, X0    ; X3 = X0 - (X2 * X1) = remainder
```

### Shifts

```asm
lsl X3, X2, #3    ; X3 = X2 << 3 (multiply by 8)
lsr X3, X2, #1    ; X3 = X2 >> 1 (divide by 2)
```

### Load and Store

```asm
ldr x0, [x1]           ; x0 = *x1 (load 8 bytes from address x1)
ldr x0, [x1, #8]       ; x0 = *(x1 + 8)
str x0, [x1]           ; *x1 = x0 (store x0 to address x1)
str X4, [X3, #0x10]    ; *(X3 + 0x10) = X4
```

### Load/Store Pair

```asm
stp X0, X1, [X3]       ; stores X0 at [X3], X1 at [X3+8]
ldp X0, X1, [X3]       ; loads X0 from [X3], X1 from [X3+8]

; Push/pop on stack
stp x29, x30, [sp, #-16]!   ; push X29, X30 (pre-decrement SP)
ldp x29, x30, [sp], #16     ; pop X29, X30 (post-increment SP)
```

Note: `stp x29, x30` saves x29 first, then x30. `ldp x29, x30` loads x29 first, then x30.

### Indexing Modes

```asm
[SP, #-16]!   ; pre-indexing: SP -= 16, then access [SP]
[SP], #16     ; post-indexing: access [SP], then SP += 16
[SP, #offset] ; offset: access [SP + offset], SP unchanged
```

### Branches

```asm
b #0x40           ; unconditional branch to PC + 0x40
br X0             ; branch to address in X0

cbz x0, label     ; branch to label if x0 == 0
cbnz x1, label    ; branch to label if x1 != 0
```

### PC-Relative Address

```asm
adr x0, my_label   ; x0 = address of my_label (PC-relative, like lea rax, [rip+offset])
```

## Function Prologue and Epilogue

```asm
; Prologue — save frame pointer and link register
stp x29, x30, [sp, #-16]!
mov x29, sp

; Epilogue — restore and return
ldp x29, x30, [sp], #16
ret
```

## Fibonacci in ARM64

```asm
fib:
    cmp X0, #1
    b.le finish

    stp x29, x30, [sp, #-0x20]!
    mov x29, sp

    sub X1, X0, #1
    str X1, [sp, #0x10]

    sub X2, X0, #2
    str X2, [sp, #0x18]

    mov X0, X1
    bl fib
    str X0, [sp, #0x10]

    ldr X2, [sp, #0x18]
    mov X0, X2
    bl fib

    ldr X3, [sp, #0x10]
    add X0, X3, X0

    ldp x29, x30, [sp], #0x20

finish:
    ret
```

## Syscalls

### Linux ARM64

```asm
mov x8, <syscall_number>   ; syscall number in x8
svc #0                     ; invoke syscall
```

Reference: https://arm64.syscall.sh/

### macOS ARM64

```asm
mov x16, 0x2000000 | <syscall_number>   ; macOS uses BSD syscall number with 0x2000000 offset
svc #0x80
```

Reference: https://github.com/opensource-apple/xnu/blob/master/bsd/kern/syscalls.master

### macOS chmod Example

```python
from pwn import *
context.arch = 'aarch64'

asm_bytes = asm("""
mov x0, #-100      ; AT_FDCWD
adr x1, flag       ; path
mov x2, #0o777     ; mode

movz x16, #0x1d3
movk x16, #0x2000, lsl #16   ; chmod syscall
svc #0x80

flag:
    .ascii "/flag\\0"
""")
```

## PAC (Pointer Authentication Codes)

PAC is a hardware security feature on ARMv8.3-A+ that prevents pointer corruption (ROP/JOP exploits). A cryptographic tag is embedded in unused pointer bits. If the tag does not match when the pointer is used, the CPU faults.

64-bit addresses use only the lower 48 bits (or 39 bits on XNU). The upper bits hold the PAC tag.

### PAC Keys

| Key | Used for |
|-----|---------|
| IA, IB | Instruction pointers (return addresses, code pointers) |
| DA, DB | Data pointers |
| GA | Generic (less common) |

PAC keys are per-process but shared across threads.

### PAC Operations

```asm
PACIA X8, X9    ; sign X8 using IA key with context X9
PACIZA X8       ; sign X8 using IA key with context 0
AUTIA X8, X9    ; authenticate X8 using IA key with context X9 — faults if invalid
XPACD x1        ; strip PAC from data pointer
BLRAA X8, X9    ; authenticate X8 using IA key with X9 context, then branch
LDRAA X8, [X9] ; authenticate X9 using DA key, load result into X8
RETAB           ; authenticate LR using IB key with SP context, then return
```

## Resources

- [arm64.syscall.sh — ARM64 Linux Syscalls](https://arm64.syscall.sh/)
- [macOS ARM64 Syscalls](https://github.com/opensource-apple/xnu/blob/master/bsd/kern/syscalls.master)
- [Azeria Labs — ARM Assembly](https://azeria-labs.com/writing-arm-assembly-part-1/)
- [PAC Research — cocomelonc](https://cocomelonc.github.io/macos/2025/07/18/malware-mac-6.html)
- [Mach IPC Security on macOS](https://karol-mazurek.medium.com/mach-ipc-security-on-macos-63ee350cb59b)
