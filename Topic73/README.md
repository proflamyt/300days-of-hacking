---
title: "Embedded Systems"
topic: "embedded-systems"
tags: [embedded, microcontroller, microprocessor, i2c, spi, uart, rtos, firmware]
difficulty: advanced
day: 73
layout: default
parent: Topics
nav_order: 73
---

# Embedded Systems

## What You Will Learn
- The difference between a microprocessor and a microcontroller
- How I2C, SPI, and UART communication protocols work
- What an RTOS interrupt is and why it matters
- How embedded security differs from regular software security

## What Is It?

An **embedded system** is a dedicated computer designed to perform specific tasks within a larger system. Examples include the controller in a microwave, the ECU in a car, or the chip inside a smartcard.

Embedded systems are everywhere — and they are increasingly connected to networks, making them targets for attackers.

## Why It Matters

- IoT devices often run embedded Linux or bare-metal RTOS
- Many embedded systems have no security updates or patching mechanism
- Firmware extraction and analysis is key to finding vulnerabilities
- Hardware attacks (JTAG, UART) are often the only way to gain initial access

## Microprocessor vs Microcontroller

| | Microprocessor | Microcontroller |
|--|---------------|----------------|
| Description | CPU only — requires external RAM, ROM, peripherals | CPU + RAM + ROM + peripherals on one chip |
| Examples | Intel Core, ARM Cortex-A | STM32, Arduino, PIC, AVR |
| Use case | General purpose computing | Embedded, real-time control |
| Cost | Higher | Lower |
| Power | Higher | Lower |

## Communication Protocols

### I2C (Inter-Integrated Circuit)

I2C is a two-wire serial protocol especially used for sensors and peripheral chips:

- **SDA** (Serial Data) — bidirectional data line
- **SCL** (Serial Clock) — clock signal from master

Devices are addressed by a 7-bit address. A master initiates all communication.

```
Master → START → ADDRESS + R/W → ACK ← Slave
Master → DATA  → ACK ← Slave
Master → STOP
```

Common I2C devices: temperature sensors, EEPROM chips, displays.

### SPI (Serial Peripheral Interface)

SPI is a four-wire full-duplex protocol for high-speed communication:

- **MOSI** (Master Out, Slave In)
- **MISO** (Master In, Slave Out)
- **SCLK** (Clock)
- **CS/SS** (Chip Select / Slave Select)

SPI is faster than I2C but uses more wires. Common for flash chips, SD cards, and ADCs.

### UART (Universal Asynchronous Receiver/Transmitter)

UART is bidirectional serial communication between exactly two nodes. It is asynchronous (no shared clock). Both sides must agree on baud rate (e.g., 115200 bps).

UART is the most common debug interface on embedded Linux systems. Connect to it with a **USB-to-serial adapter** to get a root shell on many IoT devices.

```bash
# Connect with minicom
minicom -D /dev/ttyUSB0 -b 115200

# Or screen
screen /dev/ttyUSB0 115200
```

## RTOS Interrupts

An **interrupt** signals the CPU that a hardware event has occurred (e.g., a button press, timer expiry, data received on UART). The CPU pauses its current work, runs the **Interrupt Service Routine (ISR)**, then resumes.

Key rules for ISRs:
- Must be **very short** — they block the scheduler
- Must not block or sleep
- Use deferred processing (FreeRTOS tasks) for heavier work

```c
// FreeRTOS example: wake a task from ISR
void UART_IRQHandler(void) {
    BaseType_t xHigherPriorityTaskWoken = pdFALSE;
    vTaskNotifyGiveFromISR(xHandleTask, &xHigherPriorityTaskWoken);
    portYIELD_FROM_ISR(xHigherPriorityTaskWoken);
}
```

## Embedded Security Testing

### JTAG

JTAG is a hardware debug interface on most chips. With a JTAG probe, you can:
- Read and write memory
- Set breakpoints and step through code
- Dump flash memory (extract firmware)
- Bypass secure boot in some cases

```bash
# OpenOCD — JTAG interface tool
openocd -f interface/jlink.cfg -f target/stm32f1x.cfg

# Read flash memory
flash read_bank 0 firmware.bin
```

### UART Debug Console

Many devices expose a root shell over UART:

```bash
# Find UART pins with a logic analyzer
# Common voltage: 3.3V logic
# Identify TX, RX, GND pins
# Connect USB-to-serial adapter
screen /dev/ttyUSB0 115200
```

### Firmware Analysis

```bash
# Extract firmware from a binary image
binwalk -e firmware.bin

# Find embedded filesystems
binwalk -A firmware.bin

# Search for passwords
grep -r "password" ./extracted_firmware/
```

## Resources

- [FreeRTOS Documentation](https://www.freertos.org/Documentation/RTOS_book.html)
- [OpenOCD — JTAG Debug](https://openocd.org/)
- [Binwalk — Firmware Analysis](https://github.com/ReFirmLabs/binwalk)
- [TryHackMe — Embedded Systems](https://tryhackme.com/)
- [Practical IoT Hacking — O'Reilly](https://www.oreilly.com/library/view/practical-iot-hacking/9781492062547/)
