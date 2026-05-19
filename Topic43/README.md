---
title: "Network Security"
topic: "network-security"
tags: [network-security, osi-model, firewall, ids, vpn, dhcp, dns, nat, protocols]
difficulty: intermediate
day: 43
layout: default
parent: Topics
nav_order: 43
---

# Network Security

## What You Will Learn
- How the OSI and DoD network models work
- What firewalls, IDS, and VPNs do
- How DHCP, DNS, and NAT work
- How to think about network security from an attacker and defender perspective

## OSI Model

Also known as the Open Systems Interconnection model. It was developed to help categorize how computers communicate with one another.

| Layer | Name | Protocol Examples |
|-------|------|------------------|
| 7 | Application | HTTP, FTP, SMTP, DNS |
| 6 | Presentation | TLS/SSL, compression |
| 5 | Session | NetBIOS, RPC |
| 4 | Transport | TCP, UDP |
| 3 | Network | IP, ICMP, OSPF |
| 2 | Data Link | Ethernet, MAC, ARP |
| 1 | Physical | Cables, Wi-Fi signals |

## DoD Model

The Department of Defense (DoD) model is a simplified version of the OSI model with four layers:

- **Process/Application layer** — Applications and protocols
- **Host-to-Host layer** — TCP/UDP, end-to-end delivery
- **Internet layer** — IP addressing and routing
- **Network Access layer** — Physical transmission

## Security Devices

### Firewall

The purpose of a firewall is to manage the types of traffic that can enter and leave a protected network. It is the first line of defense in protecting internal networks from outside threats.

- **Stateless Inspection**: Examines every packet individually; does not maintain state between packets
- **Stateful Inspection**: Tracks active connections; only examines the state of a connection and stores information about active network connections

### IDS (Intrusion Detection System)

An IDS identifies when a network breach or attack has occurred.

- **Signature-Based**: Detects known attack patterns
- **Anomaly-Based**: Detects deviations from normal behavior
- **Policy-Based**: Detects violations of security policy

Reference: [Protocol-Based Intrusion Detection](https://github.com/proflamyt/Protocol-Based-Intrusion-Detection)

### VPN

A VPN (Virtual Private Network) facilitates an encrypted connection to a private network over the internet. A remote host will be seen as a private host.

Types:
- **Site-to-site VPN**: Connects two office networks
- **Remote-access VPN**: Individual user connects to corporate network
- **SSL VPN**: Uses web browser, operates at Layer 7

VPN Protocols:

| Protocol | Description |
|----------|-------------|
| **IPSec** | Uses AH (authentication) or ESP (authenticate + encrypt). One-to-one only |
| **GRE** | Generic Routing Encapsulation. Supports one-to-many |
| **PPTP** | Point-to-Point Tunneling Protocol. Supports dial-up |
| **TLS 1.2/1.3** | Considered safe. Uses asymmetric encryption |
| **SSL 3.0** | Older, considered unsafe |

## Optimization and Performance Devices

- **Load Balancers**: Distribute workload across multiple servers (example: nginx)
- **Proxy Server**: Requests resources on behalf of client machines. Can filter traffic and cache content (example: nginx, Squid)

## DHCP

**Dynamic Host Configuration Protocol** assigns IP addresses to hosts on a network.

**How DHCP works:**

1. A new computer sends a DHCP discovery packet to `255.255.255.255` (broadcast) on UDP port 67
2. The DHCP server replies to the MAC address of the requesting computer with an offer packet on UDP port 68
3. The new computer sends a request packet back to the DHCP server
4. The DHCP server replies with an acknowledgment containing IP address, subnet, gateway, and DNS info
5. The computer updates its network settings

## DNS

Matches human-readable names to IP addresses.

DNS server types:

| Type | Description |
|------|-------------|
| **Root Server** | Knows where all TLD servers are |
| **TLD Server** | Handles `.com`, `.org`, `.net`, etc. |
| **Authoritative** | Has the actual DNS records for a domain |
| **Non-Authoritative** | Caches responses (recursive resolver) |

## NAT

**Network Address Translation** maps private IP addresses to public ones:

- **Static NAT**: One-to-one mapping of public to private IP
- **Dynamic NAT**: Maps from a pool of public addresses

## Resources

- [Cloudflare — How DNS Works](https://www.cloudflare.com/learning/dns/what-is-dns/)
- [TryHackMe — Network Security](https://tryhackme.com/room/networksec)
- [VICE — Undersea Cable Surveillance](https://www.vice.com/en/article/wnnmv9/undersea-cable-surveillance-is-easy-its-just-a-matter-of-money)
- [HackTricks — Network Services Pentesting](https://book.hacktricks.xyz/network-services-pentesting)
