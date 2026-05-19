---
title: "UEFI Internals and Debugging"
topic: "uefi-internals"
tags: [uefi, ovmf, edk2, gdb, firmware-debugging, pci, map-file]
difficulty: advanced
day: 92
layout: default
parent: Topics
nav_order: 92
---

# UEFI Internals and Debugging

## What You Will Learn
- What `.map` files and `.debug` files tell you about a UEFI binary
- How to debug UEFI firmware with GDB and OVMF
- What PCI is and how it appears in UEFI
- How to find a module's base address and set breakpoints in UEFI code

## What Is It?

UEFI firmware runs before the operating system. Debugging it requires different techniques than debugging a regular userspace program. This topic covers hands-on UEFI debugging using **OVMF** (the open-source UEFI for virtual machines) and **GDB**.

See [Topic90 — Firmware and UEFI Security](../Topic90/) for broader context on UEFI boot phases, Secure Boot, and firmware rootkits.

## Why It Matters

- Finding and exploiting UEFI vulnerabilities requires the ability to debug firmware
- Security researchers need to understand how UEFI modules are loaded and where they live in memory
- UEFI vulnerability research is an active field — CVE-2021-28216, PixieFail (2024), and many more
- OVMF allows safe research without risking real hardware

## Map Files and Debug Files

When OVMF is compiled in DEBUG mode, it produces two key files for every module:

```
Build/OvmfX64/DEBUG_GCC5/Ovmf.map
Build/OvmfX64/DEBUG_GCC5/X64/PeiCore.debug
```

### What Each File Contains

```
.map  → "where everything is placed"
         Shows the base address and size of every section in the final binary
         Shows which symbols (functions/variables) are at which offsets

.debug → "what everything means internally"
          Contains DWARF debug info: function names, variable names, source line numbers
          Used by GDB to map addresses to source code
```

The `.map` file gives you the layout. The `.debug` file gives you the symbols. Together they allow GDB to show you `function_name` instead of a raw address.

## Debugging UEFI with GDB

### Step 1: Start OVMF in QEMU with GDB stub enabled

```bash
qemu-system-x86_64 \
  -bios Build/OvmfX64/DEBUG_GCC5/FV/OVMF.fd \
  -nographic \
  -serial mon:stdio \
  -s -S
  # -s: enable GDB stub on port 1234
  # -S: pause at startup, wait for GDB to attach
```

### Step 2: Find the base address of the module you want to debug

```bash
# Get PeiCore's base address from the map file
grep PeiCore Build/OvmfX64/DEBUG_GCC5/Ovmf.map
```

This shows you where in memory UEFI loaded the PeiCore module.

### Step 3: Get the debug section offset

```bash
# Find the .text section offset in the .debug file
objdump -h Build/OvmfX64/DEBUG_GCC5/X64/PeiCore.debug
```

The `.text` section offset tells you how far from the module base the executable code starts.

### Step 4: Attach GDB and load symbols

```bash
gdb
(gdb) target remote :1234
(gdb) add-symbol-file Build/OvmfX64/DEBUG_GCC5/X64/PeiCore.debug <base_addr + text_offset>
(gdb) break PeiCore
(gdb) continue
```

### Automation Script

The OVMF build system provides a GDB helper script:

```bash
# Generate the GDB script from the build output
python OvmfPkg/Scripts/GdbX64.py \
  Build/OvmfX64/DEBUG_GCC5/Ovmf.map \
  Build/OvmfX64/DEBUG_GCC5/X64/ \
  > /tmp/ovmf_gdb.gdb

gdb -x /tmp/ovmf_gdb.gdb
```

This script loads all module symbols automatically.

## PCI in UEFI

**PCI (Peripheral Component Interconnect)** is a bus standard that lets components like network cards, USB controllers, GPUs, and storage controllers communicate with the CPU and memory.

In UEFI:
- UEFI enumerates PCI devices during the DXE phase
- PCI devices can have option ROMs — firmware that runs inside UEFI
- **PCI option ROM exploitation** is a real attack surface: a malicious NIC can inject code into the UEFI environment

### PCI Address Space

Each PCI device is identified by a **Bus:Device.Function** address:

```
00:00.0  Host bridge
00:02.0  VGA controller
00:1f.2  SATA controller
```

In UEFI, you can enumerate PCI devices using the `EFI_PCI_IO_PROTOCOL`:

```c
// Enumerate all PCI devices
EFI_HANDLE *HandleBuffer;
UINTN HandleCount;
gBS->LocateHandleBuffer(
    ByProtocol,
    &gEfiPciIoProtocolGuid,
    NULL,
    &HandleCount,
    &HandleBuffer
);
```

### Security Relevance

- A malicious PCI option ROM can hook UEFI boot services
- PCIe DMA attacks allow direct memory access — bypassing the CPU entirely
- IOMMU (Intel VT-d / AMD-Vi) protects against rogue DMA
- Check IOMMU status with CHIPSEC

```bash
# Check IOMMU/VT-d status
sudo python -m chipsec.main -m common.vtd
```

## UEFI Protocol Pointers

UEFI services are accessed through protocol interfaces. When debugging, these are important:

| Protocol | GUID | Purpose |
|----------|------|---------|
| `EFI_BOOT_SERVICES` | — | AllocatePool, LocateProtocol, LoadImage, etc. |
| `EFI_RUNTIME_SERVICES` | — | GetVariable, SetVariable, ResetSystem |
| `EFI_SIMPLE_TEXT_OUTPUT_PROTOCOL` | — | Print to console |
| `EFI_LOADED_IMAGE_PROTOCOL` | — | Get loaded image base address |
| `EFI_PCI_IO_PROTOCOL` | — | Access PCI device registers |

## Resources

- [EDK2 Wiki — How to Debug OVMF with GDB](https://github.com/tianocore/tianocore.github.io/wiki/How-to-debug-OVMF-with-QEMU-using-GDB)
- [UEFI Specification](https://uefi.org/specifications)
- [CHIPSEC — UEFI Security Testing](https://github.com/chipsec/chipsec)
- [PixieFail — UEFI Network Stack Vulnerabilities (2024)](https://www.quarkslab.com/blog/pixiefail-nine-vulnerabilities-in-tianocores-edk-ii-ipv6-network-stack.html)
- [Attacking UEFI with PCIe Option ROMs](https://www.troopers.de/troopers19/agenda/7af9jf/)
