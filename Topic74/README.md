---
title: "Memory Paging and Virtual Memory"
topic: "paging"
tags: [paging, virtual-memory, x86-64, cr3, page-table, kernel, memory-management]
difficulty: advanced
day: 74
layout: default
parent: Topics
nav_order: 74
---

# Memory Paging and Virtual Memory

## What You Will Learn
- What virtual memory is and why modern systems use it
- How 32-bit and 64-bit paging structures work
- How the CPU walks page tables to translate virtual to physical addresses
- How the `cr3` register relates to paging

## What Is It?

**Paging** is how modern operating systems implement **virtual memory**. Every process thinks it has a contiguous address space (e.g., 0 to 2^48), but the OS maps each virtual page to a physical page frame in RAM. This provides isolation between processes and allows more memory to be used than physically exists (via swapping).

Understanding paging is essential for kernel exploitation, hypervisor research, and understanding KASLR.

## Why It Matters

- Kernel exploits often manipulate page tables to map memory or bypass protections
- Understanding virtual-to-physical translation helps with heap and stack layouts
- KPTI, SMEP, and SMAP protections all rely on page table bits
- Virtual address leaks are critical primitives in many exploits

## Virtual Memory Addressing

In a virtual memory system:
- The CPU uses the **virtual address** in instructions
- The **Memory Management Unit (MMU)** translates virtual → physical
- The OS sets up **page tables** that describe this mapping
- Each process has its own set of page tables (its own "view" of memory)

## 32-bit Paging

In 32-bit (x86) mode without PAE:
- Virtual address space: 4 GB (2^32)
- Page size: 4 KB
- Two-level page table: **Page Directory** → **Page Table** → Physical frame

Each virtual address is split:
- Bits 31–22: Page Directory index (1024 entries)
- Bits 21–12: Page Table index (1024 entries)
- Bits 11–0: Offset within page (4096 bytes)

## 64-bit Paging

In 64-bit (x86-64) mode:
- 512 entries per level
- **4-level page table** structure
- Page table base register: **`cr3`** — holds the physical address of the PGD

```gdb
# Get cr3 value in GDB
p/x $cr3 & ~0xfff
```

### PML4 Walking (4-Level Paging)

```
Virtual Address → PML4 → PDPT → PD → PT → Physical Frame
```

Full names:
- **PML4**: Page Map Level 4 (also called PGD — Page Global Directory)
- **PDPT**: Page Directory Pointer Table (also called PUD — Page Upper Directory)
- **PD**: Page Directory (also called PMD — Page Middle Directory)
- **PT**: Page Table

The 64-bit virtual address is split:

| Bits | Name | Description |
|------|------|-------------|
| 63–48 | Sign extension | Must match bit 47 |
| 47–39 | PML4 index | Selects entry in PML4 table |
| 38–30 | PDPT index | Selects entry in PDPT |
| 29–21 | PD index | Selects entry in PD |
| 20–12 | PT index | Selects entry in PT |
| 11–0 | Page offset | Offset within 4KB page |

### Page Table Entry

Each entry in a page table holds:
- Bits 51–12: Physical page frame address (40 bits)
- Bit 0 (P): Present — is the page in physical memory?
- Bit 1 (R/W): Read/Write permission
- Bit 2 (U/S): User/Supervisor — is user-mode access allowed?
- Bit 63 (XD/NX): Execute Disable — is execution from this page forbidden?

### Walking the PML4 in GDB

```gdb
# 1. Get physical address of PGD from cr3
p/x $cr3 & ~0xfff

# 2. Use PML4 index (bits 47-39) to get PDPT pointer
# Each entry is 8 bytes

# 3. Use PDPT index (bits 38-30) to get PD pointer
# Getting PUD from bits 12 to 51 of the entry

# 4. Continue until you reach the final physical address in the Page Table entry
```

### Linux Kernel Page Table Notation

In Linux kernel source code:

```c
// PGD = PML4 in x86-64
pgd_t *pgd = pgd_offset(mm, address);

// PUD = PDPT
pud_t *pud = pud_offset(pgd, address);

// PMD = PD
pmd_t *pmd = pmd_offset(pud, address);

// PTE = PT entry
pte_t *pte = pte_offset_map(pmd, address);
```

## Protection Mechanisms Using Paging

- **SMEP (Supervisor Mode Execution Prevention)**: Bit in `cr4`. The kernel cannot execute code from user-space pages.
- **SMAP (Supervisor Mode Access Prevention)**: Bit in `cr4`. The kernel cannot access user-space memory without explicitly setting the `AC` flag.
- **KPTI (Kernel Page Table Isolation)**: Separates kernel page tables from user-space page tables to mitigate Meltdown.
- **NX bit**: Page table entry bit — prevents code execution from data pages.

## Resources

- [OSDev — Paging](https://wiki.osdev.org/Paging)
- [Intel SDM Vol. 3 — Paging](https://www.intel.com/content/www/us/en/developer/articles/technical/intel-sdm.html)
- [Linux Kernel Memory Management](https://www.kernel.org/doc/html/latest/admin-guide/mm/index.html)
- [pwn.college — Kernel Security](https://pwn.college/)
