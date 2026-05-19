---
title: "Linux Kernel Exploitation"
topic: "kernel-exploitation"
tags: [kernel, exploitation, linux, heap, slab, kaslr, smep, smap, lpe]
difficulty: advanced
day: 77
layout: default
parent: Topics
nav_order: 77
---

# Linux Kernel Exploitation

## What You Will Learn
- How the Linux kernel heap (SLUB allocator) works
- Common kernel heap primitives and API functions
- How KASLR, SMEP, and SMAP protect the kernel
- How kernel hardening mitigations work

## What Is It?

**Kernel exploitation** is the process of exploiting vulnerabilities in the OS kernel to gain the highest possible privilege — root or ring-0 access. Kernel bugs can give an attacker full control of a system, bypassing all user-space security controls.

## Why It Matters

- Kernel vulnerabilities are used in privilege escalation from container escapes
- Local privilege escalation (LPE) bugs often live in the kernel
- CTF pwn challenges frequently involve kernel exploitation
- Malware often uses kernel exploits for persistence and evasion

## Kernel Heap API

### Creating Kernel Objects

```c
// Create a proc entry (exposes interface in /proc)
proc_create(name, mode, parent, &fops);

// Create a cache with a region suitable for copying to userspace
kmem_cache_t *cache = kmem_cache_create(
    "cache_name",       // name
    object_size,        // size of each object
    0,                  // alignment
    SLAB_HWCACHE_ALIGN,
    NULL                // constructor
);

// Allocate an object from a specific cache
void *obj = kmem_cache_alloc(cache, GFP_KERNEL);
// Returns pointer to new object, or NULL on error
```

### Copying Between User and Kernel Space

```c
// Copy from user space into kernel space
unsigned long copy_from_user(
    void *to,                   // kernel destination
    const void __user *from,    // user source
    unsigned long n             // bytes to copy
);

// Copy from kernel space to user space
unsigned long copy_to_user(
    void __user *to,            // user destination
    const void *from,           // kernel source
    unsigned long n             // bytes to copy
);
```

### Inspecting the Slab Allocator

```bash
# View slab cache information
sudo cat /proc/slabinfo
```

## Kernel Heap Structure

The Linux kernel uses the **SLUB allocator**. Caches are backed by pages:
- Each cache holds objects of a specific size
- A cache may contain multiple **slabs** (backed by pages)
- Example: a cache of size 512 may have slabs with 8 objects each (512 × 8 = 4096 bytes = one page)

## Kernel Heap Hardening

Modern kernels have several heap protections:

### SLUB Allocation Randomization

Allocations within a slab are returned in a random order, making heap feng-shui harder.

### Hardened Usercopy

Validates that `copy_to_user`/`copy_from_user` operations are within expected bounds — prevents kernel stack leaks.

### Freelist Hardening

The `next` pointer in the freelist is mangled to prevent corruption from being directly useful:

```
mangled_ptr = REV(ptr) XOR ptr_addr XOR random_secret
```

To follow a freelist, an attacker must know the `random_secret` — which requires an info leak.

### Freelist Randomization

When allocating objects from slabs, the slots are returned in random order.

### Free List Poisoning

Overwriting the `next` pointer in a freed chunk can cause the next allocation to return a controlled address — the foundation of heap exploitation.

## Kernel Protections (CPU-level)

### KASLR (Kernel Address Space Layout Randomization)

Randomizes the kernel's base address at boot. An attacker needs an **info leak** (reading kernel memory) to bypass this.

```bash
# Check KASLR status
cat /proc/sys/kernel/kptr_restrict
```

### SMEP (Supervisor Mode Execution Prevention)

The kernel cannot execute code from user-space pages. Prevents `ret2usr` attacks where the attacker places shellcode in user space and jumps to it from the kernel.

Controlled by bit 20 of `cr4`.

### SMAP (Supervisor Mode Access Prevention)

The kernel cannot access user-space memory without explicitly clearing the `AC` flag. Prevents kernel code from inadvertently using attacker-controlled user-space data.

Controlled by bit 21 of `cr4`.

### Defeating SMEP/SMAP

```asm
; Disable SMEP and SMAP by clearing bits in cr4
mov rax, cr4
and rax, ~(1<<20 | 1<<21)   ; clear bits 20 (SMEP) and 21 (SMAP)
mov cr4, rax
```

## kmalloc Internals

```bash
# Reference: kmalloc internal workings
# http://www.jikos.cz/jikos/Kmalloc_Internals.html
```

The `kmalloc()` function allocates memory from specific size-ordered caches:
- `kmalloc-8`, `kmalloc-16`, `kmalloc-32`, ... up to `kmalloc-8192`
- For larger allocations, contiguous pages are allocated directly

## Resources

- [Linux Kernel Exploitation Workshop](https://github.com/paboldin/kernel-exploit-workshop)
- [Linux Kernel CVEs](https://cve.mitre.org/cgi-bin/cvekey.cgi?keyword=linux+kernel)
- [pawnyable.cafe — Kernel Exploitation](https://pawnyable.cafe/)
- [kmalloc Internals](http://www.jikos.cz/jikos/Kmalloc_Internals.html)
- [TryHackMe — Linux Kernel Exploitation](https://tryhackme.com/)
