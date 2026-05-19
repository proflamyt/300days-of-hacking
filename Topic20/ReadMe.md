---
title: "Process Injection"
topic: "process-injection"
tags: [process-injection, dll-injection, windows, malware, evasion, reflective-dll]
difficulty: advanced
day: 20
layout: default
parent: Topics
nav_order: 20
---

# Process Injection

## What You Will Learn
- What processes, applications, and services are on Windows
- What process injection is and why attackers use it
- The most common process injection techniques
- Which Windows processes are most commonly targeted

Before we dig into process injection, let's understand what a process, an application, and a service are.

## What Is an Application?

An application is a program you interact with on the desktop. This is where most users spend their time — Google Chrome, MS Word, iTunes, Skype are all applications.

## What Is a Service?

A service is a process that runs in the background and does not interact with the desktop. Some services run before the user has even logged in.

Services can be viewed through **Task Manager → Services**.

Under the "Startup Type" column, they are classified as:

- **Automatic**: Started at boot time.
- **Automatic (Delayed)**: Started after almost everything else has powered up.
- **Manual**: Started by a user or specific circumstances.
- **Disabled**: Should not run at all.

## What Is a Process?

A process is an instance of a particular executable (`.exe`) running. A given application may have several processes running simultaneously. For example, major browsers like Chrome and Firefox run several processes at once — each tab, utility, and extension is a separate instance of the same executable.

Each process has its own private virtual memory space (a sandbox) that is isolated from other processes. Inside this memory space, you can find:

- The process executable
- Its list of loaded modules (DLLs or shared libraries)
- Its stacks, heaps, and allocated memory regions containing everything from user input to application-specific data structures

## What Is a Handle?

A handle is an integer value that identifies a thread, registry key, file, or process to Windows. Handles should be released after use (with `CloseHandle()`), just like you would call `free()` after `malloc()`. If you do not release a handle to a resource after use, other processes may not be able to access it — this is why you sometimes cannot delete a file because Windows claims it is in use.

`_EPROCESS` is the name of the structure that Windows uses to represent a process. SIDs (Security Identifiers) are used by the kernel to enforce security and access control.

## What Is It?

**Process Injection** (also known as Code Injection) is a method of executing arbitrary code in the address space of a separate, live process.

Some antivirus defenses rely on process names to detect malware. Adversaries started injecting code into legitimate processes to evade these defenses — the malicious code runs under the name of a trusted process like `explorer.exe` or `svchost.exe`.

Running code in the context of another process may allow:
- Access to the target process's memory
- Access to system/network resources
- Possibly elevated privileges

There are also legitimate uses for process injection — debuggers use it to hook into applications, and antivirus programs often inject code into browsers to monitor network traffic and block dangerous content.

## Processes Targeted by Adversaries

Windows processes commonly used by threat actors:

- **Common software**: `iexplore.exe`, `chrome.exe`, `firefox.exe`, `outlook.exe`
- **Built-in Windows processes**: `explorer.exe`, `svchost.exe`, `regsvr32.exe`, `dllhost.exe`, `services.exe`, `msbuild.exe`, `rundll32.exe`, `PowerShell.exe`, `cmd.exe`

## Process Injection Techniques

According to MITRE ATT&CK, there are 11 process injection techniques for Windows, Linux, and macOS. Here are the 4 most common:

### 1. Classic DLL Injection via CreateRemoteThread and LoadLibrary

The malware writes the path to its malicious DLL in the virtual address space of another process, and creates a remote thread in the target process to load it.

Steps:
1. Open the target process with `OpenProcess()`
2. Allocate memory in the target process with `VirtualAllocEx()`
3. Write the DLL path into that memory with `WriteProcessMemory()`
4. Create a remote thread to call `LoadLibrary()` with `CreateRemoteThread()`

### 2. Remote DLL Injection

A malicious process forces the target process to load a specified DLL from disk by calling `LoadLibrary` or the native `LdrLoadDll`. The DLL must exist on disk before injection.

### 3. PE (Portable Executable) Injection

The malware injects a malicious PE image into an already-running process. This is a disk-less operation — the malware does not need to write its payload to disk before injection. The PE handles its own relocation and execution.

### 4. Reflective DLL Injection

A malicious process writes a DLL (as a sequence of bytes) into the memory space of a target process. The DLL handles its own initialization — mapping itself into memory, resolving imports, and running `DllMain` — all without using the Windows loader. The DLL does not need to exist on disk.

### 5. Process Hollowing

A malicious process starts a new instance of a legitimate process (e.g., `svchost.exe`) in a suspended state. It then unmaps the legitimate code from memory and replaces it with the malicious payload. When the process is resumed, it executes the malicious code entirely.

## Resources

- [Elastic — Ten Process Injection Techniques](https://www.elastic.co/blog/ten-process-injection-techniques-technical-survey-common-and-trending-process)
- [MITRE ATT&CK — Process Injection (T1055)](https://attack.mitre.org/techniques/T1055/)
- [TryHackMe — Windows Internals](https://tryhackme.com/room/windowsinternals)
