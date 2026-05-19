---
title: "Linux Privilege Escalation"
topic: "linux-privilege-escalation"
tags: [linux, privilege-escalation, sudo, suid, sgid, kernel, enumeration]
difficulty: intermediate
day: 4
layout: default
parent: Topics
nav_order: 4
---

# Privilege Escalation (Linux)

## What You Will Learn
- What privilege escalation is and why it matters after gaining initial access
- How SUDO, SUID, SGID, kernel exploits, and PATH abuse work
- Manual enumeration commands to find escalation vectors
- How to use GTFOBins to abuse allowed commands

Most times when you gain remote shell access, it's very unlikely you gain access as a privileged user. You'll probably gain access as a low-level user. As a low-level user, what you can do on the system is restricted (this is for a good security reason). Your access to certain sensitive files is restricted; there are limits to what changes you can make and what you can install. Generally, a user like that is only given access to what they need to perform their tasks and nothing more.

Think of this as a company hierarchy. There's the lowest user who has a boss that has a boss, where the highest boss (we know them as **root** here) can do anything. There you are, a very low-privilege user in a corner office whose job is just to write a document — with little or no say in the workings of the company, no access to the company's files except your own.

But does that mean this low-level access is useless? No. This is where **privilege escalation** comes in — we look for a vulnerability or misconfiguration to gain access as a more privileged user or as root. There are different ways we can go about this. I'll take you through some manual enumeration and exploitation and update this as time goes by. There are also tools like **linPEAS** that handle automatic enumeration — do check it out.

## Introduction

### SUDO

Remember the highest boss we mentioned? The one who has access to everything — that's the **root** user. Allowing them to handle everything can be very risky. As root, you can create, install, delete, and modify any file. So you have to be very careful with this privileged power!

To handle everyday tasks without always acting as root, **SUDO** was introduced. Sudo stands for **SuperUser DO** and is used to access restricted files and operations. Think of sudo as a staff of authority — it lets you execute a command temporarily as a **super user** who belongs to the sudoers group. In some cases it allows you to execute commands even as the root user itself.

### SETUID

SETUID (Set User ID) is a special file permission that allows a file to be executed with the privileges of its owner rather than the user running it. If a binary has SUID set and is owned by root, it runs as root regardless of who executes it. This is a common privilege escalation vector when misconfigured.

### SGID

SGID (Set Group ID) works similarly to SUID, but at the group level. When set on an executable, the process runs with the group permissions of the file's group owner rather than the group of the user executing it. When set on a directory, new files created inside inherit the directory's group — useful for shared directories.

### Kernel Exploitation

If the system is running an outdated kernel, there may be public kernel exploits that allow a low-privilege user to escalate to root. Tools like `linux-exploit-suggester` can identify vulnerable kernel versions automatically.

```bash
uname -r          # check kernel version
searchsploit linux kernel <version>   # search for public exploits
```

Example: Dirty Cow (CVE-2016-5195) is a well-known kernel privilege escalation exploit.

### PATH Hijacking

In Linux, the `PATH` is an environment variable that tells the operating system where to search for executables. If a privileged program runs another program using a relative path (e.g., `service` instead of `/usr/sbin/service`), an attacker who controls the `PATH` can place a malicious binary earlier in the path and have it executed with elevated privileges.

```bash
echo $PATH     # view current PATH
export PATH=/tmp:$PATH   # place /tmp at the front
echo '/bin/bash' > /tmp/service && chmod +x /tmp/service
```


## Enumeration

### Check for Listening Ports

```bash
netstat -lt          # list listening TCP ports
netstat -s           # list network usage statistics by protocol
```

### Find Files with the SUID Bit Set

```bash
find / -perm -u=s -type f 2>/dev/null
```

### Check If User Can Execute Specific Commands with Root Privilege

```bash
sudo -l
```

Then use [GTFOBins](https://gtfobins.github.io/) to find exploitation methods for allowed commands.

### Check Kernel Version

```bash
uname -r
```

### List Files That Have SUID or SGID Bits Set

```bash
find / -type f -perm -04000 -ls 2>/dev/null
```

### Use `getcap` to List Enabled Capabilities

```bash
getcap -r / 2>/dev/null
```

### Check Crontab

```bash
cat /etc/crontab
```

### Check Environment PATH Variables

```bash
echo $PATH
```

### Find Folders with Writable Access

```bash
find / -type d -writable -print
find / -writable 2>/dev/null | cut -d "/" -f 2,3 | grep -v proc | sort -u
```

### Check for Mount with `no_root_squash` Enabled

```bash
showmount -e <IP>
```

## Resources

- [GTFOBins](https://gtfobins.github.io/) — Exploit allowed sudo binaries for privilege escalation
- [LinPEAS](https://github.com/carlospolop/PEASS-ng) — Automated Linux privilege escalation enumeration
- [Linux Exploit Suggester](https://github.com/mzet-/linux-exploit-suggester)
- [TryHackMe — Linux PrivEsc Room](https://tryhackme.com/room/linprivesc)
