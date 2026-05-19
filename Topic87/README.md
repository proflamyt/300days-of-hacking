---
title: "Miscellaneous Security Concepts"
topic: "miscellaneous"
tags: [c, linker, constructor, init-array, pe, elf, low-level]
difficulty: advanced
day: 87
layout: default
parent: Topics
nav_order: 87
---

# Miscellaneous Security Concepts

## What You Will Learn
- How GCC constructors run before `main()`
- How the C runtime initialization chain works
- What the `__attribute__((packed))` directive does
- How these concepts relate to exploit development

## What Is It?

This topic covers low-level C and linker concepts that are important for malware analysis, binary exploitation, and reverse engineering.

## Why It Matters

Understanding how programs initialize before `main()` is critical for:
- Reverse engineering obfuscated binaries that hide logic in constructors
- Writing shellcode that hooks into the initialization chain
- Understanding how shared library hijacking works (DLL/SO injection)

## GCC Constructor Attribute

The `__attribute__((constructor))` directive marks a function to run **before** `main()`. The linker places it in the `.init_array` section.

```c
void __attribute__((constructor)) run_before_main() {
    write(1, "hello", 6);
}
```

When this program runs, `"hello"` is printed before anything in `main()` executes. This is used by:
- Shared library initialization code
- Malware that hides in `.init_array`
- Sanitizers (ASAN, UBSAN) that need early initialization

## C Runtime Initialization Chain

When a Linux ELF binary starts, execution flows:

```c
_start
 └── __libc_start_main
       └── __libc_csu_init
             └── iterate .init_array   ← runs all constructors here
                   └── main()
```

`__libc_csu_init` iterates through the `.init_array` section, calling each function pointer. This is why constructor functions run before `main()`.

### In Reverse Engineering

When analyzing a binary, always check:

```bash
# List .init_array entries
readelf -S binary | grep init_array
objdump -d -j .init_array binary

# List all function pointers in .init_array
objdump --section=.init_array -s binary
```

Malware often places its real entry point in `.init_array` to run before any debugger breakpoints set on `main`.

## Packed Structures

The `__attribute__((packed))` directive tells GCC to use the **exact size** of the struct with no padding bytes between members:

```c
struct normal {
    char a;      // 1 byte + 3 bytes padding
    int  b;      // 4 bytes
};  // sizeof = 8

struct __attribute__((packed)) packed {
    char a;      // 1 byte (no padding)
    int  b;      // 4 bytes
};  // sizeof = 5
```

This is used in:
- Network protocol parsing (packets have exact formats)
- File format parsing
- Binary protocol implementations

Unintended use of packed structs (vs. non-packed) is a source of memory corruption bugs — if you copy a packed struct's address into a function expecting aligned access, you get an alignment fault.

## Other GCC Attributes Used in Security

```c
// Mark a function as never returning (like exit())
void __attribute__((noreturn)) fatal_error(void);

// Mark a function as deprecated
void __attribute__((deprecated)) old_func(void);

// Declare a function with specific visibility
void __attribute__((visibility("hidden"))) internal_func(void);

// Enforce a specific section placement
void __attribute__((section(".text.hot"))) hot_path(void);

// Prevent inlining (useful for stack frame analysis)
void __attribute__((noinline)) do_something(void);
```

## Sections in ELF/PE

| Section | Contents |
|---------|---------|
| `.text` | Executable code |
| `.data` | Initialized global variables |
| `.bss` | Uninitialized global variables |
| `.rodata` | Read-only data (string literals) |
| `.init_array` | Function pointers called before main |
| `.fini_array` | Function pointers called after main |
| `.plt` | Procedure Linkage Table (dynamic symbol stubs) |
| `.got` | Global Offset Table (dynamic symbol addresses) |

## Resources

- [GCC Attributes Reference](https://gcc.gnu.org/onlinedocs/gcc/Function-Attributes.html)
- [ELF Format Specification](https://man7.org/linux/man-pages/man5/elf.5.html)
- [Linux From Scratch — Program Initialization](https://tldp.org/HOWTO/Program-Library-HOWTO/index.html)
- [pwn.college — Binary Exploitation](https://pwn.college/)
