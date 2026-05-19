---
title: "Heap Exploitation"
topic: "heap-exploitation"
tags: [heap, ptmalloc, tcache, fastbin, use-after-free, double-free, heap-overflow, pwn]
difficulty: advanced
day: 72
layout: default
parent: Topics
nav_order: 72
---

# Heap Exploitation

## What You Will Learn
- How glibc's heap allocator (ptmalloc2) organizes free memory
- What tcache, fastbins, smallbins, and largebins are
- How Use-After-Free (UAF) and double-free vulnerabilities work
- The maximum sizes for each bin type

## What Is It?

The **heap** is where dynamically allocated memory lives (via `malloc`/`free`). When memory is freed, glibc organizes it into **bins** based on size for quick reuse. Heap exploitation involves corrupting these structures to gain control of memory allocation.

## Why It Matters

Heap exploitation is a core technique in:
- Modern CTF pwn challenges
- Browser exploitation (Chrome, Firefox)
- Kernel exploitation
- Real-world CVE exploitation

## Heap Bin Types

### tcache (Thread-Local Cache)

- Singly linked list with **mangled pointers**
- Maximum of **7 chunks per bin**
- Per-thread — each thread has its own tcache
- **Maximum chunk size**: 1032 bytes (`0x408`) on x86_64
- Freed chunks go here first; malloc checks here first

### Fastbins

- Singly linked list with safe-linking (similar to tcache)
- Bin lists can grow to unlimited length
- Fixed-size chunks up to **128 bytes (`0x80`)**
- The `P` (previous in-use) bit is never cleared
- Only checks the top chunk for double-free detection

### Unsorted Bins

- Freed chunks that do not fit in tcache or fastbins land here first
- On the next `malloc`, if no chunk satisfies the request, chunks get sorted into small or large bins
- Chunks may be consolidated (merged with adjacent free chunks)

### Small Bins

- Doubly linked list
- Fixed-size chunks up to **1024 bytes (`0x400`)**

### Large Bins

- Doubly linked lists, stored in **sorted order**
- Each chunk has forward (`fd`) and backward (`bk`) pointers
- Size up to the `mmap_threshold` (~128 KB by default)

### Maximum Chunk Sizes (x86_64)

| Allocation Type | Max Chunk Size |
|----------------|---------------|
| **TCache** | 1032 bytes (`0x408`) |
| **Fastbin** | 128 bytes (`0x80`) |
| **Smallbin** | 1024 bytes (`0x400`) |
| **Largebin** | Up to `mmap_threshold` (~128 KB) |
| **mmap** | Several TB (limited by virtual memory) |

Chunks larger than `mmap_threshold` bypass the heap entirely and are allocated via `mmap()`.

## Common Heap Vulnerabilities

### Use-After-Free (UAF)

Use-After-Free occurs when a program continues to use a pointer after the memory it points to has been freed.

```c
a = malloc(128);      // allocate chunk
free(a);              // free it — chunk goes to tcache
scanf("%d", a);       // write to freed chunk (overwrites tcache fd pointer)
password_pointer = malloc(128);  // malloc returns our controlled chunk
printf("%s", password_pointer);  // we control what this prints
```

An attacker controlling the freed chunk can set the `fd` pointer to any address — the next `malloc` returns that address.

### Double Free

Freeing the same chunk twice corrupts the bin's linked list.

```c
a = malloc(128);
free(a);         // a goes to tcache
a[1] = 1234;     // overwrite the tcache fd pointer with a target address
free(a);         // free again — corrupt the tcache list
// Next two mallocs: first returns a normally, second returns address 1234
```

Modern glibc has mitigations against double-free — tcache checks for double-free by checking if the chunk is already at the head of the bin.

## Heap Hardening

Modern glibc includes several protections:

- **SLUB allocation randomization**: Random ordering in slab allocation
- **Hardened Usercopy**: Validates copies between user space and kernel space
- **Freelist hardening**: Mangles `next` pointers: `rev(ptr) ^ ptr_addr ^ random`
- **Freelist randomization**: Objects are returned in random order from slabs
- **Free list poisoning**: Overwrite the `next` pointer — if the chunk is allocated, returns your controlled address

## Useful Commands

```bash
# View heap in GDB with pwndbg
heap
bins

# Show tcache contents
tcache

# Check free list state
vis_heap_chunks
```

## Resources

- [Toddler's Introduction to Heap Exploitation Part 1](https://infosecwriteups.com/the-toddlers-introduction-to-heap-exploitation-part-1-515b3621e0e8)
- [Toddler's Introduction to Heap Exploitation Part 2](https://infosecwriteups.com/the-toddlers-introduction-to-heap-exploitation-part-2-d1f325b74286)
- [how2heap — Heap Exploitation Techniques](https://github.com/shellphish/how2heap)
- [glibc malloc internals](http://www.jikos.cz/jikos/Kmalloc_Internals.html)
- [pwn.college — Heap Exploitation](https://pwn.college/)
