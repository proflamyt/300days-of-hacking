---
title: "LLDB"
topic: "lldb"
tags: [lldb, debugger, macos, ios, arm64, reverse-engineering, xcode]
difficulty: intermediate
day: 82
layout: default
parent: Topics
nav_order: 82
---

# LLDB

## What You Will Learn
- How to use LLDB to debug macOS and iOS binaries
- How to disassemble functions, read/write registers and memory
- How to set breakpoints and step through code
- How to use LLDB for reverse engineering

## What Is It?

**LLDB** is Apple's debugger, included with Xcode. It is the standard debugger for macOS, iOS, and other Apple platforms. LLDB is similar to GDB but uses a different command syntax and integrates deeply with Apple's toolchain.

LLDB is essential for macOS/iOS security research, app analysis, and jailbreak development.

## Basic Commands

### Disassembly

```lldb
# Disassemble the main function
disas -n main

# Disassemble at the current program counter
disas -s $pc

# Disassemble with number of instructions
disas -s $pc -c 20
```

### Reading Sections and Memory Layout

```lldb
# Show all memory sections of the current binary
image dump sections

# Show image list (loaded binaries and their base addresses)
image list

# Find the load address of a specific function
image lookup -n functionName
```

### Registers

```lldb
# Read all registers
register read

# Read a specific register
register read x0

# Write to a register
register write x0 0x100e98060
```

### Memory

```lldb
# Read 4 bytes at an address as integer
memory read --size 4 0x16f9c7a6c

# Write 4 bytes to an address
memory write --size 4 0x16f9c7a6c 0x31337

# Alternative: use expr to write through a cast
expr *(int*)0x16f9c7a6c = 0x31337

# Read a string at an address
memory read --format c 0x100001234
```

### Breakpoints

```lldb
# Break at a function name
breakpoint set -n main
b main

# Break at an address
b 0x100001234

# List breakpoints
breakpoint list

# Delete a breakpoint
breakpoint delete 1

# Disable / enable
breakpoint disable 1
breakpoint enable 1
```

### Stepping

```lldb
# Step into (follows calls)
step
s

# Step over (does not enter calls)
next
n

# Step one instruction
stepi
si

# Step over one instruction
nexti
ni

# Continue execution
continue
c

# Finish current function
finish
```

### Expression Evaluation

```lldb
# Call a function from the debugger
expr (void)printf("hello\n")

# Cast and call
expr (NSString *)[[NSString alloc] initWithUTF8String:"test"]

# Calculate
expr (int)(0x100 + 0x10)
```

## LLDB Scripting with Python

```python
import lldb

def breakpoint_handler(frame, bp_loc, dict):
    print("Breakpoint hit!")
    print("PC:", hex(frame.GetPC()))
    return False
```

## Attaching to a Running Process

```lldb
# Attach by process name
process attach --name MyApp

# Attach by PID
process attach --pid 1234
```

## Remote Debugging (iOS)

```lldb
# On iOS device, run debugserver
debugserver *:1234 /path/to/app

# On Mac, connect with LLDB
process connect connect://device-ip:1234
```

## Useful One-Liners

```lldb
# Print all arguments to a function at a breakpoint
b -n malloc
command add
  frame variable
DONE

# Watch a memory address for writes
watchpoint set expression -- &variable
```

## Resources

- [LLDB Tutorial — lldb.llvm.org](https://lldb.llvm.org/use/tutorial.html)
- [LLDB Quick Reference](https://developer.apple.com/library/archive/documentation/IDEs/Conceptual/gdb_to_lldb_transition_guide/document/lldb-command-examples.html)
- [Frida — Runtime Instrumentation on iOS](https://frida.re/)
- [iPhoneDevWiki — Debugging](https://iphonedev.wiki/index.php/Debugging)
- [TryHackMe — iOS Security](https://tryhackme.com/)
