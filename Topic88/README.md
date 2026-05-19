---
title: "Hardware Hacking"
topic: "hardware-hacking"
tags: [hardware-hacking, jtag, fault-injection, side-channel, uart, boot-rom, embedded]
difficulty: advanced
day: 88
layout: default
parent: Topics
nav_order: 88
---

# Hardware Hacking

## What You Will Learn
- What hardware hacking involves and what targets are typical
- How JTAG and UART debug interfaces work
- How fault injection is used in hardware attacks
- How side-channel analysis works on physical hardware

## What Is It?

**Hardware hacking** is the security assessment of physical electronic devices. It involves probing hardware interfaces, extracting firmware, and exploiting physical vulnerabilities. Common targets include:
- IoT devices (routers, smart speakers, cameras)
- Payment terminals and ATMs
- Smartcards and secure elements
- Industrial control systems

Hardware attacks often succeed where software-only attacks fail — because the hardware exposes interfaces that bypass software security.

## Why It Matters

- Hardware vulnerabilities cannot be patched with a software update
- Many devices ship with debug interfaces enabled
- Firmware extraction is the first step to finding vulnerabilities at scale
- Physical security is the foundation of all security

## JTAG

**JTAG (Joint Test Action Group)** is an industry standard hardware debug interface. Almost every modern chip has a JTAG interface used during manufacturing test. When left accessible in production devices, it gives an attacker:

- Full memory read/write access
- Ability to set breakpoints and step through code
- Firmware extraction
- Bypass of secure boot in some cases

```
JTAG Pins:
TDI  - Test Data In
TDO  - Test Data Out
TMS  - Test Mode Select
TCK  - Test Clock
TRST - Test Reset (optional)
```

### JTAG Tools

```bash
# OpenOCD — universal JTAG interface tool
openocd -f interface/jlink.cfg -f target/stm32f1x.cfg

# Connect to target and dump flash
telnet localhost 4444
> flash read_bank 0 firmware.bin 0 0

# GDB over OpenOCD
arm-none-eabi-gdb
(gdb) target remote :3333
(gdb) monitor reset halt
(gdb) x/10i $pc
```

## UART Debug Console

**UART (Universal Asynchronous Receiver/Transmitter)** is the most common debug interface on embedded Linux devices. Many IoT devices expose a root shell over UART during boot.

### Finding UART Pins

UART typically uses 3.3V logic. Use a multimeter or oscilloscope to identify:
- **TX** (transmit) — toggles during boot
- **RX** (receive)
- **GND** (ground, 0V)

VCC is usually present but not needed.

### Connecting

```bash
# Connect with USB-to-serial adapter
screen /dev/ttyUSB0 115200

# Or minicom
minicom -D /dev/ttyUSB0 -b 115200

# Common baud rates: 115200, 9600, 57600, 38400
```

## Boot ROM

The **Boot ROM** is the first code that runs when a chip powers on. It is mask-ROM — burned into the chip during manufacturing and cannot be changed. Boot ROM vulnerabilities are among the most serious hardware security bugs, as they can be used to jailbreak devices.

Notable Boot ROM exploits:
- **checkm8** (iPhone): Boot ROM exploit affecting A5–A11 chips
- **CVE-2017-13293**: U-Boot secure boot bypass

## Fault Injection

See [Topic85 — Fault Injection](../Topic85/) for detailed coverage.

Hardware fault injection targets:
- Secure boot verification (skip signature check)
- PIN/password verification (skip comparison)
- Cryptographic key generation (weaken randomness)

## Side Channel Analysis

See [Topic34 — Side Channel Attacks](../Topic34/) for detailed coverage.

Hardware side channels include:
- **Power analysis**: Measure current drawn during cryptographic operations
- **Electromagnetic analysis**: Measure EM emissions
- **Timing analysis**: Measure how long operations take

### Basic Power Measurement Setup

```
Target Device → Shunt Resistor (1Ω) → Ground
                      ↓
                  Oscilloscope (measures voltage across shunt = current)
                      ↓
                  ChipWhisperer / Custom ADC
```

## Firmware Extraction

Even without JTAG, firmware can be extracted from flash chips:

```bash
# Identify the flash chip on the PCB
# Common chips: Winbond W25Q128, Macronix MX25L12835F

# Desolder or clip the flash chip
# Use flashrom to read it
flashrom -p linux_spi:dev=/dev/spidev0.0,spispeed=1000 -r firmware.bin

# Analyze the firmware
binwalk -e firmware.bin
strings firmware.bin | grep -i password
```

## Resources

- [ChipWhisperer — Hardware Security Training](https://www.newae.com/chipwhisperer)
- [OpenOCD — JTAG/SWD Debugger](https://openocd.org/)
- [Flashrom — Flash Chip Programming](https://www.flashrom.org/)
- [Practical IoT Hacking Book](https://nostarch.com/practical-iot-hacking)
- [TryHackMe — Hardware Hacking](https://tryhackme.com/room/hardwarehacking101)
