---
title: "Firmware and UEFI Security"
topic: "firmware-security"
tags: [firmware, uefi, bios, secure-boot, bootkit, embedded-security]
difficulty: advanced
day: 90
layout: default
parent: Topics
nav_order: 90
---

# Firmware and UEFI Security

## What You Will Learn
- What firmware is and why it is a high-value attack target
- How UEFI replaced BIOS and what the boot process looks like
- What Secure Boot does and how attackers bypass it
- How firmware rootkits achieve the deepest possible persistence
- How to analyze and extract firmware

## What Is It?

**Firmware** is low-level software stored in non-volatile memory (flash chips) on hardware devices. It runs before the operating system and controls the hardware directly.

**UEFI (Unified Extensible Firmware Interface)** is the modern replacement for the legacy BIOS. It is a full software environment — it has drivers, a network stack, and can run EFI applications before the OS loads.

Firmware is the most privileged code on a machine. An attacker with firmware-level persistence:
- Survives OS reinstalls
- Survives hard drive replacement
- Can modify the OS before it loads
- Is invisible to most security tools

## Why It Matters

- Firmware rootkits like **LoJax**, **MoonBounce**, and **CosmicStrand** have been found in real-world attacks
- UEFI vulnerabilities can bypass Secure Boot entirely
- Nation-state actors target firmware for long-term persistence
- Once firmware is compromised, there is no guaranteed remediation short of hardware replacement

## UEFI Boot Process

```
Power On
  └── CPU reset vector → UEFI firmware in SPI flash
        └── SEC (Security Phase)
              └── PEI (Pre-EFI Initialization)
                    └── DXE (Driver Execution Environment)
                          └── BDS (Boot Device Selection)
                                └── Bootloader (GRUB / Windows Boot Manager)
                                      └── OS Kernel
```

Each phase hands off to the next. Attackers target the DXE phase — it is where most UEFI drivers load, and a malicious DXE driver can persist across reboots.

## Secure Boot

**Secure Boot** is a UEFI feature that verifies every component in the boot chain has a trusted cryptographic signature before executing it.

```
UEFI firmware → checks signature of bootloader
Bootloader → checks signature of OS kernel
OS kernel → checks signatures of kernel modules
```

Keys involved:
- **PK (Platform Key)**: Root of trust, owned by the hardware vendor
- **KEK (Key Exchange Key)**: Used to update the signature database
- **db (Signature Database)**: Hashes/keys of trusted boot software
- **dbx (Forbidden Signature Database)**: Revoked signatures

### Secure Boot Bypasses

```bash
# Check Secure Boot status on Linux
mokutil --sb-state

# Common bypass techniques:
# 1. Exploit a vulnerability in a signed bootloader (BootHole — GRUB2 CVE-2020-10713)
# 2. Enroll a custom key if the system allows custom MOK enrollment
# 3. Exploit a UEFI vulnerability to modify the db/dbx
# 4. Physical attack: clear NVRAM and re-enroll keys
```

## Firmware Rootkits

A firmware rootkit modifies UEFI to load malicious code before the OS. It does this by inserting a malicious DXE driver into the UEFI image stored in SPI flash.

**Real-world examples:**
- **LoJax** (APT28, 2018): First UEFI rootkit found in the wild — modified UEFI to drop a Windows agent after every reboot
- **MoonBounce** (2022): Implanted in the SPI flash of a laptop's UEFI — survived OS reinstall
- **CosmicStrand** (2022): Targeted the CSMCORE DXE driver in ASUS motherboard firmware

### Persistence Mechanism

```
Malicious DXE driver in SPI flash
  └── Runs at boot (before OS loads)
        └── Hooks OS loader in memory
              └── Drops malware into OS on every boot
```

## Firmware Analysis

```bash
# Extract firmware from a live Linux system (Intel)
sudo fwupdmgr get-devices
sudo fwupdmgr get-updates

# Dump UEFI firmware from SPI flash using flashrom
flashrom -p internal -r firmware.bin

# Analyze UEFI firmware with UEFITool
# (GUI tool — open firmware.bin and inspect modules)

# Extract and analyze with uefi-firmware-parser
pip install uefi-firmware-parser
uefi-firmware-parser -e firmware.bin -O output_dir/

# Analyze with binwalk
binwalk -e firmware.bin

# Check for known vulnerabilities with fwcheck or CHIPSEC
pip install chipsec
sudo python -m chipsec.main
```

## EDK2 and OVMF

**EDK2** is the open-source UEFI firmware development kit. **OVMF** is a UEFI firmware for virtual machines (built from EDK2).

```bash
# Build OVMF from source
git clone https://github.com/tianocore/edk2.git
cd edk2
git submodule update --init
make -C BaseTools
source edksetup.sh
build -a X64 -t GCC5 -p OvmfPkg/OvmfPkgX64.dsc

# Run OVMF in QEMU
qemu-system-x86_64 \
  -bios Build/OvmfX64/DEBUG_GCC5/FV/OVMF.fd \
  -nographic \
  -serial mon:stdio
```

## Defense

- **Enable Secure Boot** and do not disable it
- **Enable BIOS/UEFI password** to prevent physical reconfiguration
- **Disable boot from USB** in UEFI settings
- **Enable TPM** — it can detect firmware tampering via measured boot
- **CHIPSEC** — open-source tool to audit UEFI security settings
- **Keep firmware updated** — vendors release patches for UEFI CVEs

## Resources

- [UEFI Specification — UEFI Forum](https://uefi.org/specifications)
- [EDK2 — Open Source UEFI Firmware](https://github.com/tianocore/edk2)
- [CHIPSEC — Firmware Security Tool](https://github.com/chipsec/chipsec)
- [UEFITool — UEFI Firmware Analysis](https://github.com/LongSoft/UEFITool)
- [LoJax Analysis — ESET Research](https://www.welivesecurity.com/2018/09/27/lojax-first-uefi-rootkit-found-wild/)
