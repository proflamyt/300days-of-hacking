---
title: "Windows Internals"
topic: "windows-internals"
tags: [windows, kernel, architecture, registry, user-mode, kernel-mode, dll]
difficulty: advanced
day: 9
layout: default
parent: Topics
nav_order: 9
---

# Windows Internals

## What You Will Learn
- The high-level architecture of Windows NT (user mode vs. kernel mode)
- What the Windows Registry is and how it is structured
- What DLLs, processes, threads, and services are
- How the Windows Executive, kernel, and HAL relate to each other
- Key Windows APIs and subsystems used by security tools

## Overview

Windows is the most widely used desktop operating system in the world. It was first released in 1985 and has had several major updates since then.

An operating system is the software that manages a computer's hardware and provides an interface for the user. Operating systems are among the most complex software in existence — they are responsible for a wide variety of tasks, ranging from managing background processes to translating human inputs into machine commands.

The Windows NT architecture consists of two main layers: **user mode** and **kernel mode**.

- Programs and subsystems in **user mode** are limited in terms of what system resources they have access to.
- **Kernel mode** has unrestricted access to system memory and external devices.

## Key Terms

### Windows API

An Application Programming Interface provided by Microsoft for interaction with the Windows operating system. It consists of thousands of documented, callable subroutines such as `CreateProcess` and `CreateFile`. Major categories include Base Services, Networking, Graphics & Multimedia, and User Interface.

### DLL (Dynamic Link Library)

A DLL is a library that contains code and data that can be used by more than one program at the same time. This facilitates code reuse.

### Windows SDK (Software Development Kit)

Header files that expose exported DLL functions to the programmer.

### Windows.h

Includes all the basic Windows SDK headers needed in a typical basic Windows application.

### User Mode

Manages processes on behalf of the user — lower privilege. User-mode processes cannot directly access hardware; they must call into kernel mode.

### Kernel Mode

The components where core OS operations run. Kernel mode has unrestricted access to the system memory and hardware.

### Windows Registry

A collection of databases that contain system configuration data. The registry stores information, settings, options, and other values for programs and hardware installed on all versions of Microsoft Windows. When a program is installed, a new subkey containing its location, version, and startup information is added to the registry.

**Key Hives:**

- `HKEY_CURRENT_USER` — Configuration info for the currently logged-on user
- `HKEY_USERS` — Active user profiles on the computer
- `HKEY_LOCAL_MACHINE` — Configuration info for the computer (machine-wide)
- `HKEY_CLASSES_ROOT` — Windows uses this to manage file type associations
- `HKEY_CURRENT_CONFIG` — Information about the hardware profile used at startup

### Processes

A process is an instance of a particular executable (`.exe`) running. It includes:

- An executable program
- A private virtual address space
- System resources accessible to all threads in the process
- A unique process ID (PID)
- At least one thread of execution
- A security context (access token)

### Threads

A thread is what Windows schedules for execution within a process. Without threads, the process cannot run. Threads consist of:

- Register contents representing the processor state
- Two stacks (one for kernel mode, one for user mode)
- A private storage area used by subsystems, run-time libraries, and DLLs
- A unique thread ID

### Windows Services

A Windows service is a computer program that operates in the background, similar in concept to a Unix daemon. Services are controlled by the Windows Service Manager and can run before any user logs in.

**Startup Types:**

- `Automatic` — Started at boot time
- `Automatic (Delayed)` — Started after almost everything else has powered up
- `Manual` — Started by a user or specific circumstances
- `Disabled` — Should not run at all

### Secure Desktop

The Secure Desktop is a separate desktop session used by Windows for UAC prompts and login screens. It prevents other processes from interacting with these security dialogs.


## Windows Architecture

The Windows NT operating system family's architecture consists of two layers: user mode and kernel mode, with many different modules within both layers.

### User Mode

User mode is made up of subsystems that can pass I/O requests to the appropriate kernel-mode device drivers through the I/O Manager. The user mode layer of Windows NT consists of:

- **Environment subsystems**: Run applications written for many different types of operating systems.
- **Integral subsystem**: Operates system-specific functions on behalf of the environment subsystems.

There are three main environment subsystems:

1. **Win32 subsystem**: Runs 32-bit Windows applications. Contains console and text window support, shutdown handling, and Virtual DOS Machines (VDMs) for running legacy MS-DOS and 16-bit Win16 applications.
2. **OS/2 subsystem**: Supports 16-bit character-based OS/2 applications (removed as of Windows XP).
3. **POSIX subsystem**: Supports applications written strictly to POSIX.1 standards. Later replaced by the Windows Subsystem for Linux (WSL).

### Kernel Mode

Kernel mode has full access to the hardware and system resources of the computer and runs code in a protected memory area. Code running in kernel mode includes:

- **The Executive** — The main kernel-mode component (contained in `NTOSKRNL.EXE`)
- **The Kernel** — Low-level services used by the Executive
- **Hardware Abstraction Layer (HAL)**
- **Kernel-mode drivers**

### The Executive

The Windows Executive services make up the low-level kernel-mode portion. It deals with I/O, object management, security, and process management. Subsystems include:

- **I/O Manager**: Allows devices to communicate with user-mode subsystems. Translates read/write commands into I/O Request Packets (IRPs).
- **Security Reference Monitor (SRM)**: Enforces security rules using Access Control Lists (ACLs) and Access Control Entries (ACEs).
- **Object Manager**: All other Executive subsystems must pass through the Object Manager to gain access to Windows resources.
- **Virtual Memory Manager**: Manages virtual memory and controls paging to/from disk.
- **Process Manager**: Handles process and thread creation and termination.
- **PnP Manager**: Handles Plug and Play and device detection at boot time.
- **Power Manager**: Deals with power events (power-off, stand-by, hibernate).
- **Cache Manager**: Works with the Memory Manager and I/O Manager to cache file I/O.
- **Configuration Manager**: Implements the system calls needed by the Windows Registry.

### The Kernel

The kernel sits between the HAL and the Executive and provides:

- Multiprocessor synchronization
- Thread and interrupt scheduling and dispatching
- Trap handling and exception dispatching
- Initialization of device drivers at bootup

### Hardware Abstraction Layer (HAL)

The HAL is a layer between the physical hardware and the rest of the operating system. It was designed to hide differences in hardware and provide a consistent platform on which the kernel is run. The HAL includes hardware-specific code that controls I/O interfaces, interrupt controllers, and multiple processors.

### Hybrid Kernel Design

The Windows NT design includes many of the same objectives as Mach, the archetypal microkernel system, including a small kernel limited to core functions such as first-level interrupt handling, thread scheduling, and synchronization primitives.


## Start Application on Boot

```
Press Windows key + R.
In the run box, type regedit, and press Enter.
Paste the following path in the address bar:
Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run

Right-click on Run and create a new String value.
Edit the name to what you want and set the value data to the program path you want to run on boot.
```


## Windows Commands

Windows has two command-line shells: the **Command shell** (cmd.exe) and **PowerShell**. Each shell provides direct communication between you and the operating system.

### Common Registry Run Keys

```powershell
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
```


## Resources

- [Windows Architecture Overview](https://medium.com/@putrasulung2108/windows-architecture-d2b022f136d3)
- [Windows Internals Book (Sysinternals)](https://learn.microsoft.com/en-us/sysinternals/resources/windows-internals)
- [TryHackMe — Windows Internals Room](https://tryhackme.com/room/windowsinternals)
