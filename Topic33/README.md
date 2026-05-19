---
title: "Security Research Methodology"
topic: "security-research"
tags: [research, methodology, vulnerability-research, bug-bounty, reconnaissance]
difficulty: intermediate
day: 33
layout: default
parent: Topics
nav_order: 33
---

# Security Research Methodology

## What You Will Learn
- How to approach security research in a structured way
- How to enumerate targets and find attack surfaces
- How to document and report findings
- Common research techniques used in bug bounty and pentesting

## What Is It?

Security research is the process of finding vulnerabilities in systems, applications, or networks. Good research is systematic — you follow a methodology so you do not miss anything.

This topic covers how to research a target from scratch. The skills here apply to bug bounty hunting, penetration testing, and competitive CTFs.

## Why It Matters

Without structure, security testing becomes guesswork. A methodology ensures:
- You cover the entire attack surface
- You document what you find
- You can reproduce and explain your findings
- You do not break anything you are not supposed to

## Key Concepts

### The Research Phases

1. **Reconnaissance** — Gather information about the target
2. **Enumeration** — Map out services, endpoints, and potential entry points
3. **Vulnerability Analysis** — Identify weaknesses in what you found
4. **Exploitation** — Confirm the vulnerability is real and exploitable
5. **Documentation** — Write up what you found, how, and why it matters

### Passive vs. Active Recon

| Type | Description | Examples |
|------|-------------|---------|
| **Passive** | No direct interaction with target | WHOIS, Shodan, Google Dorking |
| **Active** | Direct interaction with target | Port scanning, directory fuzzing |

## Hands-On

### Enumerate a Target

```bash
# WHOIS lookup
whois example.com

# DNS enumeration
dig example.com ANY
subfinder -d example.com

# Port scan
nmap -sV -p- example.com

# Directory brute force
ffuf -w /usr/share/wordlists/dirb/common.txt -u https://example.com/FUZZ
```

### Finding Attack Surfaces

```bash
# Find subdomains
amass enum -d example.com

# Search for exposed files
google dork: site:example.com filetype:pdf

# Find JavaScript files and endpoints
katana -u https://example.com
```

### Testing Router and IoT Firmware

When researching embedded devices like routers:

```bash
# Extract firmware
binwalk -e firmware.bin

# Look for hardcoded credentials
grep -r "password" ./extracted_firmware/
grep -r "admin" ./extracted_firmware/

# Find web interfaces
find . -name "*.cgi" -o -name "*.php"
```

### Documentation Template

When you find something, document it:

```
Title: [Short description]
Severity: Critical / High / Medium / Low
Target: [URL or component]

Description:
[What the vulnerability is]

Steps to Reproduce:
1. Go to...
2. Enter...
3. Observe...

Impact:
[What an attacker can do]

Suggested Fix:
[How the developer should fix it]
```

## Resources

- [HackerOne — Bug Bounty Platform](https://hackerone.com/)
- [Bugcrowd — Bug Bounty Platform](https://bugcrowd.com/)
- [OWASP Testing Guide](https://owasp.org/www-project-web-security-testing-guide/)
- [NahamSec — Bug Bounty Methodology](https://github.com/nahamsec/Resources-for-Beginner-Bug-Bounty-Hunters)
- [Project Discovery Tools](https://projectdiscovery.io/)
