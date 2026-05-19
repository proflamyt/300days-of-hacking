---
title: "Windows and Networking"
topic: "windows-networking"
tags: [windows, networking, smb, ntlm, kerberos, ntfs, permissions, registry, wmi]
difficulty: intermediate
day: 28
layout: default
parent: Topics
nav_order: 28
---

# Windows and Networking

## What You Will Learn
- How to enumerate Windows systems using WMI and PowerShell
- How Windows file system permissions work with icacls
- What the Windows Registry is and how it is used for persistence
- What SAM, UAC, WMI, and Security Identifiers (SIDs) are
- How SMB sharing and Kerberos/NTLM authentication work

## Introduction to Windows

### Useful WMI Classes for Enumeration

```powershell
Get-WmiObject -Class win32_OperatingSystem   # OS information
Get-WmiObject -Class win32_Bios              # BIOS information
Get-WmiObject -Class win32_Service           # Running services
Get-WmiObject -Class win32_Process           # Running processes
```

### Windows Directory Structure

| Directory | Purpose |
|-----------|---------|
| `Perflogs` | Windows performance logs |
| `Program Files` | Installed 64-bit program files |
| `Program Files (x86)` | Installed 32-bit program files |
| `ProgramData` | Application data shared across users |
| `Users` | User profile directories |
| `Windows` | Core Windows OS files |
| `Windows\System32` | Core 64-bit DLLs and system executables |
| `Windows\SysWOW64` | 32-bit compatibility DLLs on 64-bit systems |

## Windows File System

Windows uses two main file systems:

- **FAT32**: Older, simpler file system. No permissions or journaling.
- **NTFS**: Modern Windows file system. Supports permissions, journaling, encryption (EFS), and large volumes.

### The icacls Utility

`icacls` lists and manages NTFS permissions on a specific directory or file.

**Inheritance flags:**

| Flag | Meaning |
|------|---------|
| `(I)` | Permission inherited from parent container |
| `(OI)` | Object inherit — this folder and files |
| `(CI)` | Container inherit — this folder and subfolders |
| `(IO)` | Inherit only — ACE does not apply to the current folder |
| `(NP)` | Do not propagate inherit |

**Combinations:**

| Combo | Scope |
|-------|-------|
| `(OI)(CI)` | This folder, files, and subfolders |
| `(CI)(IO)` | Subfolders only |
| `(OI)(IO)` | Files only |
| `(OI)(CI)(IO)` | Files and subfolders only |

**File permissions:**

| Flag | Permission |
|------|-----------|
| `(F)` | Full access |
| `(M)` | Modify access |
| `(RX)` | Read and execute access |
| `(R)` | Read-only |
| `(W)` | Write-only |
| `(D)` | Delete access |
| `(N)` | No access |

```powershell
# List permissions
icacls <directory>

# Remove permissions
icacls <directory> /remove <user>:<permission>

# Grant permissions
icacls <directory> /grant <user>:<permission>
```

### Windows Service Commands

```powershell
# Query a service
sc qc <servicename>

# Stop a service
sc stop <servicename>

# Configure a service
sc configure <servicename> <configuration>
```

## Windows Users

The built-in Administrator account is not the most powerful account in Windows. The most powerful is the **SYSTEM** user account — this is the Windows equivalent of root in Linux.

### Service Accounts

| Account | Privilege | Description |
|---------|-----------|-------------|
| `NT AUTHORITY\LocalService` | Limited | Limited local system access |
| `NT AUTHORITY\NetworkService` | Limited + network | Can authenticate to network services |
| `NT AUTHORITY\SYSTEM` | Highest | Full system access |

### Windows Sessions

- **Interactive Session**: A session created when a user logs in at the console or via RDP.
- **Non-Interactive Session**: Account with no password (used for services and scheduled tasks).

## Windows WMI

Windows Management Instrumentation is used for:

- Code execution
- Scheduling processes
- Setting up logging
- Managing user and group permissions
- Modifying and setting system properties

```cmd
wmic os list brief
```

```powershell
Get-WmiObject -Class Win32_OperatingSystem
```

## Windows Security Identifier (SID)

SIDs are unique IDs stored in the security database that Windows uses to identify users on a system. They are assigned at account creation and never reused.

## Windows SAM

The **Security Account Manager** is a registry file on Windows that stores local user account password hashes. The file is stored at `C:\Windows\system32\config`. It is not accessible while Windows is running — Windows keeps an exclusive lock on it until the computer is shut down.

```bash
# Extract SAM hash (from offline system or shadow volume)
reg save hklm\sam %tmp%/sam.reg
```

## Windows UAC (User Account Control)

UAC is a Windows security feature that prevents unauthorized changes to the operating system. When an app tries to perform a privileged action, UAC prompts the user for approval. Attackers try to bypass UAC to escalate privileges silently.

## Windows Registry

The registry stores system and application configuration in a hierarchical key-value database.

**Common value types:**

| Type | Description |
|------|-------------|
| `REG_BINARY` | Binary data |
| `REG_DWORD` | 32-bit integer |
| `REG_QWORD` | 64-bit integer |
| `REG_SZ` | Null-terminated Unicode or ANSI string |
| `REG_EXPAND_SZ` | String with unexpanded environment variable references |

**Persistence registry keys:**

```powershell
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

## Windows API

Windows APIs allow user applications to interact with the operating system, separated into:

- System Services
- Multimedia
- Networking
- User Interface
- Window Registry

### Evading Malware Detection (Awareness)

Common techniques attackers use to bypass AV/EDR:

- Syscalls (bypassing hooked APIs)
- Use of ordinals (calling DLL functions by number, not name)
- Hooks (redirecting execution flow)
- IAT patching (modifying the Import Address Table)

### IAT (Import Address Table)

The IAT contains the list of DLLs, function names, and function addresses that a PE (Portable Executable) depends on to run.

## Windows Rights and Privileges

- **Rights**: Deal with permission to access objects such as files.
- **Privileges**: Grant users permission to perform an action, such as running a program with elevated access.

## SMB Shares

**Server Message Block (SMB)** is a networking protocol that allows file sharing and storage among users. It uses a client-server relationship and operates on port 445. A user can remotely access a file share even without being in the physical location of the server. It supports both anonymous and password-protected authentication.

```bash
# Enumerate SMB shares
smbclient -L //<IP> -U username

# Connect to a share
smbclient //<IP>/SHARENAME -U username
```

## Privilege Escalation Using PsExec

Download PsExec from Windows PsTools:

```cmd
psexec -sid cmd.exe
```

## Resources

- [SS64 — icacls Reference](https://ss64.com/nt/icacls.html)
- [TryHackMe — Windows Fundamentals](https://tryhackme.com/room/windowsfundamentals1xbx)
- [HackTricks — Windows Privilege Escalation](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation)
