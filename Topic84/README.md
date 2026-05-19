---
title: "Bluetooth Security"
topic: "bluetooth-security"
tags: [bluetooth, ble, gatt, pairing, piconet, wireless, iot-security]
difficulty: intermediate
day: 84
layout: default
parent: Topics
nav_order: 84
---

# Bluetooth Security

## What You Will Learn
- How Bluetooth and BLE (Bluetooth Low Energy) work
- The pairing process and how devices authenticate each other
- What GATT, L2CAP, and BLE Mesh are
- Common Bluetooth attack techniques

## What Is It?

**Bluetooth** is a short-range wireless communication standard. **BLE (Bluetooth Low Energy)** is a variant optimized for very low power consumption — it is used in wearables, IoT sensors, medical devices, and smart locks.

Bluetooth operates in the ISM band from 2.402 GHz to 2.480 GHz.

## BLE Characteristics

- Very low power consumption
- Low bandwidth
- Fast setup
- Range: typically 10–30 meters, up to 100 meters in some cases

## How Bluetooth Pairing Works

The first step in establishing a Bluetooth connection is **pairing**:

1. One device makes itself **discoverable** and broadcasts its presence to nearby Bluetooth devices
2. The second device receives this broadcast and sends a **pairing request** to the broadcasting device
3. Both devices **authenticate each other** using a link key or long-term key (LTK)
4. Once paired, the devices store each other's details — they do not need to pair again for future connections

## Bluetooth Network Topology

Bluetooth devices form a communication ring called a **piconet**, where there is one **master** device and up to seven active **slave** devices.

### Link Types

| Type | Description |
|------|-------------|
| **SCO (Synchronous Connection-Oriented)** | Used for audio — reserves slots at regular intervals for steady uninterrupted communication |
| **ACL (Asynchronous Connection-Less)** | Used for all other data — transmits whenever bandwidth allows |

## Key Protocols and Terms

| Term | Description |
|------|-------------|
| **L2CAP** | Logical Link Control and Adaptation Protocol — provides higher-level protocol multiplexing and packet segmentation |
| **Object Push Profile (OPP)** | Profile for sending files between Bluetooth devices |
| **HCI** | Host Controller Interface — communication between host and Bluetooth controller |
| **SDP** | Service Discovery Protocol — allows devices to find available services |

## GATT (Generic Attribute Profile)

GATT defines how BLE devices communicate data. It uses a **server/client** model:

- **Server**: Device that holds data (e.g., a heart rate sensor)
- **Client**: Device that reads data (e.g., your phone)

Data is organized as:
- **Services**: Groups of related data (e.g., Heart Rate Service)
- **Characteristics**: Individual data points within a service (e.g., Heart Rate Measurement)
- **Descriptors**: Metadata about characteristics

Each service and characteristic has a **unique UUID** (either 16-bit for standard or 128-bit for custom).

Reference: https://www.bluetooth.com/specifications/assigned-numbers/

## BLE Mesh Proxy

BLE Mesh allows many BLE devices to form a network (not just point-to-point). The Mesh Proxy exposes:
- **DATA IN**: Accepts data from the client (write)
- **DATA OUT**: Sends data to the client (notify)

## Common Bluetooth Attacks

### Reconnaissance

```bash
# Scan for Bluetooth devices
hciconfig hci0 up
hcitool scan          # classic Bluetooth
hcitool lescan        # BLE scan

# Or use bluez
bluetoothctl
scan on
```

### BLE GATT Enumeration

```bash
# Install gatttool
sudo apt install bluez

# Connect and enumerate services
gatttool -b <MAC_ADDRESS> --interactive
  connect
  primary          # list services
  characteristics  # list characteristics
  char-read-hnd 0x0025  # read a characteristic by handle
```

### BlueSmacking (DoS)

Sends oversized L2CAP packets to crash a device.

### Bluesnarfing

Unauthorized access to a Bluetooth device to steal contacts, messages, or files through OBEX Push Profile vulnerabilities.

### KNOB Attack (Key Negotiation of Bluetooth)

Reduces Bluetooth encryption key entropy to 1 byte, making brute-force trivial.

### BLE Security Modes

| Mode | Description |
|------|-------------|
| No security | Unencrypted, unauthenticated |
| Unauthenticated encryption | Encrypted but no MITM protection |
| Authenticated encryption | Uses passkey or OOB pairing — protects against MITM |

## Resources

- [Bluetooth Assigned Numbers](https://www.bluetooth.com/specifications/assigned-numbers/)
- [Nordic Semiconductor — BLE Fundamentals](https://devzone.nordicsemi.com/guides/short-range-guides/b/bluetooth-low-energy/posts/ble-characteristics-a-beginners-tutorial)
- [BlueZ — Linux Bluetooth Stack](http://www.bluez.org/)
- [TryHackMe — Bluetooth Security](https://tryhackme.com/)
- [KNOB Attack](https://knobattack.com/)
