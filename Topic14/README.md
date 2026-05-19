---
title: "Active Directory"
topic: "active-directory"
tags: [active-directory, windows, kerberos, ntlm, ldap, smb, domain-controller]
difficulty: intermediate
day: 14
layout: default
parent: Topics
nav_order: 14
---

# Active Directory

## What You Will Learn
- What Active Directory is and how it organizes a Windows domain
- How NTLM and Kerberos authentication work step by step
- What LDAP, SMB, and MS-RPC are and how they are used in AD
- Common attacks against Active Directory environments

## What Is It?

Active Directory (AD) is Microsoft's directory service used to manage users, computers, and resources in a Windows domain environment. It is central to most enterprise networks — which makes it the primary target during internal penetration tests.

## Domain Controller

A **Windows domain** is a form of computer network in which all user accounts, computers, printers, and other security principals are registered with a central database located on one or more clusters of central computers known as **domain controllers**.

## Key Terms

- **Objects**: Any resource within AD (users, computers, printers, groups).
- **Attributes**: Characteristics of an object (e.g., a user's email address or phone number).
- **Domain**: A group of objects managed under the same AD database.
- **Forest**: A collection of one or more AD domains that share a common schema and global catalog.
- **Global Unique Identifier (GUID)**: A 128-bit value assigned to every object in AD to uniquely identify it.
- **Security Principals**: Objects that run in the context of a user or computer account (used for access control).

## PowerShell Commands

```powershell
# Get information about a specific computer
Get-ADComputer <computername>

# Get information about all domain controllers
Get-ADDomainController
```

> `Get-ADDomainController` gets information about the domain controllers in Active Directory.

## NTLM Authentication Process

NTLM (New Technology LAN Manager) is a Microsoft authentication protocol. It uses a challenge-response mechanism instead of sending passwords in plain text.

1. The user shares their username, password, and domain name with the client.
2. The client creates a hash of the password and deletes the full password.
3. The client passes a plain-text version of the username to the relevant server.
4. The server replies to the client with a **challenge** — a 16-byte random number.
5. The client sends the challenge encrypted by the hash of the user's password.
6. The server sends the challenge, response, and username to the domain controller (DC).
7. The DC retrieves the user's password hash from the database and uses it to encrypt the challenge.
8. The DC compares the encrypted challenge with the client's response. If they match, the user is authenticated.

![NTLM](https://github.com/proflamyt/300days-of-hacking/blob/main/Topic14/pictures/c9113ad0ff443dd0973736552e85aa69.png)

### NTLM Attacks

1. **Brute-forcing**: Trying many passwords against the NTLM hash offline after extracting it.
2. **Password Spraying**: Trying a single common password against many accounts to avoid lockouts.
3. **Pass-the-Hash**: Authenticating using a captured NTLM hash without cracking it.

## Kerberos Authentication

Kerberos is the primary authentication protocol used in modern Active Directory environments. It is more secure than NTLM and uses tickets instead of passwords.

1. The user shares their username, password, and domain name with the client.
2. The client creates an **authenticator** (encrypted with the user's password hash) and sends it to the KDC (Key Distribution Center).
3. The KDC checks the username and decrypts the authenticator using the user's stored password hash. If successful, the user's identity is verified.
4. The KDC issues a **Ticket Granting Ticket (TGT)**, which is encrypted and sent to the client.
5. The client stores the TGT in its Kerberos cache. It is valid for 8 hours by default.
6. When the client needs to access a resource, it sends the TGT to the KDC and requests a **service ticket**.
7. The KDC generates a service ticket encrypted with the target server's key and sends it to the client.
8. The client presents the service ticket to the target server.
9. The server decrypts the ticket with its own password. If successful, access is granted.

### Kerberos Attacks

- **Kerberoasting**: Requesting service tickets for accounts with SPNs (Service Principal Names) and cracking them offline.
- **AS-REP Roasting**: Targeting accounts that do not require Kerberos pre-authentication.
- **Pass-the-Ticket**: Using a stolen Kerberos ticket to authenticate as a user.
- **Golden/Silver Ticket**: Forging Kerberos tickets using extracted secrets.

## LDAP (Lightweight Directory Access Protocol)

LDAP is the protocol used to query and modify Active Directory. It operates over port 389 (and 636 for LDAPS — LDAP over SSL).

```bash
# Query AD using ldapsearch
ldapsearch -x -H ldap://<DC_IP> -b "dc=domain,dc=local" "(objectClass=user)"
```

Attackers use LDAP to enumerate users, groups, computers, and other AD objects during reconnaissance.

## MS-RPC (Microsoft Remote Procedure Call)

MS-RPC is a protocol that allows a program to request a service from a program on another computer in a network. In AD environments, it is used for:

- Replication between domain controllers
- Remote management (WMI, WinRM)
- Service communication

Many AD attacks (such as exploiting the Netlogon vulnerability — Zerologon, CVE-2020-1472) leverage MS-RPC.

## SMB (Server Message Block)

SMB is a network file-sharing protocol that allows applications to read and write to files and request services from server programs. It operates on port 445 (and historically 139).

In AD environments, SMB is used for:
- File sharing across the domain
- Remote service management
- Printer sharing

**Common SMB attacks:**
- **EternalBlue (MS17-010)**: A critical SMB vulnerability used by WannaCry ransomware.
- **SMB Relay**: Capturing and replaying NTLM authentication over SMB.
- **Pass-the-Hash over SMB**: Using NTLM hashes to authenticate to SMB shares.

```bash
# List SMB shares
smbclient -L //<IP> -U username

# Connect to a share
smbclient //<IP>/SHARENAME -U username
```

## Relative IDs (RIDs)

Each object in an AD domain has a Security Identifier (SID). The last part of the SID is the Relative ID (RID), which identifies the specific object:

```
500  — Administrator account
501  — Guest account
512  — Domain Admins group
513  — Domain Users group
514  — Domain Guests group
1000+ — Regular user accounts start here
```

## Resources

- [CrowdStrike — NTLM Authentication](https://www.crowdstrike.com/cybersecurity-101/ntlm-windows-new-technology-lan-manager/)
- [HackTricks — Active Directory](https://book.hacktricks.xyz/windows-hardening/active-directory-methodology)
- [TryHackMe — Active Directory Basics](https://tryhackme.com/room/winadbasics)
- [BloodHound — AD Attack Path Tool](https://github.com/BloodHoundAD/BloodHound)
