---
title: "OSINT"
topic: "osint"
tags: [osint, reconnaissance, passive-recon, google-dorking, whois]
difficulty: beginner
day: 7
layout: default
parent: Topics
nav_order: 7
---

# OSINT

## What You Will Learn
- What OSINT is and why it is the first step in any penetration test
- The difference between passive and active reconnaissance
- Key OSINT tools and websites used by security professionals
- How to use Google Dorking to find sensitive information
- How to gather information on a target without touching their systems

## What Is It?

**OSINT** stands for **Open Source Intelligence**. It is the practice of collecting information from publicly available sources. In security and penetration testing, OSINT is the first step — you gather as much information about a target as possible before ever touching their systems.

"Open source" in this context does not mean open-source software. It means publicly accessible information: websites, social media, DNS records, public databases, job listings, and more.

## Why It Matters

Before launching any attack, a penetration tester needs to know:

- Who owns the target domain?
- What IP addresses and services are exposed?
- Who works at the company? (Useful for social engineering.)
- What software stack is the target running?

OSINT answers these questions **without directly touching the target**. This is called **passive reconnaissance**. It is legal because you are not interacting with the target's systems — you are only looking at publicly available data.

## Key Concepts

### Passive vs. Active Reconnaissance

- **Passive recon**: Gathering information without directly contacting the target. This is OSINT. No logs on the target's systems.
- **Active recon**: Directly interacting with the target system (e.g., port scanning). This leaves traces and can be detected.

### What Can You Find with OSINT?

- Domain registration details (WHOIS)
- Subdomains and IP addresses
- Employee names and email addresses
- Technologies used by the target (Wappalyzer, Shodan)
- Past data breaches
- Social media profiles and leaked credentials

## Hands-On

### Useful OSINT Tools and Websites

**Domain and IP Intelligence**

- [Threat Intelligence Platform](https://threatintelligenceplatform.com) — Investigate domains and IPs for threat data
- [ViewDNS](https://viewdns.info) — DNS lookup tools, reverse IP lookup, WHOIS history

**WHOIS Lookup**

```bash
whois example.com
```

**Shodan — Search Engine for Devices**

Shodan indexes internet-connected devices. You can find web servers, cameras, industrial control systems, and more.

```bash
# Install Shodan CLI
pip install shodan

# Search for Apache servers in Nigeria
shodan search "apache country:NG"
```

**DNS Enumeration**

```bash
# Find DNS records
dnsrecon -d example.com -t std

# Brute-force subdomains
gobuster dns -d example.com -w /usr/share/wordlists/subdomains-top1million-5000.txt
```

**Email Harvesting**

```bash
# theHarvester — gather emails, names, subdomains, IPs
theHarvester -d example.com -l 500 -b google
```

**Google Dorking**

Google dorking uses advanced search operators to find sensitive information that is indexed publicly.

```
site:example.com filetype:pdf
intitle:"index of" site:example.com
inurl:admin site:example.com
"password" filetype:txt site:example.com
```

**Social Media and Breach Data**

- [HaveIBeenPwned](https://haveibeenpwned.com) — Check if an email was in a data breach
- [Hunter.io](https://hunter.io) — Find email addresses tied to a domain

## Resources

- [Threat Intelligence Platform](https://threatintelligenceplatform.com)
- [ViewDNS Tools](https://viewdns.info)
- [OSINT Framework](https://osintframework.com) — A massive collection of OSINT tools organized by category
- [Shodan](https://www.shodan.io)
- [TryHackMe — Google Dorking Room](https://tryhackme.com/room/googledorking)
- [theHarvester GitHub](https://github.com/laramies/theHarvester)
