---
title: "Threads and Processes"
topic: "threads-processes"
tags: [threads, processes, concurrency, linux, scheduling, ipc, race-condition]
difficulty: intermediate
day: 36
layout: default
parent: Topics
nav_order: 36
---

# Threads and Processes

## What You Will Learn
- The difference between a process and a thread
- How the OS schedules threads
- How threads communicate and share memory
- How race conditions arise and why they matter in security

## What Is It?

A **process** is an independent running program with its own memory space. A **thread** is a unit of execution within a process. Multiple threads share the same memory space but run concurrently.

Understanding processes and threads is essential for exploit development, privilege escalation, and understanding how operating systems work at a low level.

## Why It Matters

Security relevance includes:
- **Race conditions** can be exploited for privilege escalation (TOCTOU bugs)
- **Thread injection** is a core technique in malware and process injection
- **Shared memory** between threads creates attack surfaces
- Debugging tools like GDB and WinDbg work at the thread/process level

## Key Concepts

### Process vs Thread

| | Process | Thread |
|--|---------|--------|
| Memory | Own address space | Shares address space with other threads |
| Creation cost | Expensive (new address space) | Cheap (same address space) |
| Communication | IPC required | Direct memory access |
| Crash impact | Isolated | Can crash whole process |

### Creating Threads in C

```c
#include <pthread.h>
#include <stdio.h>

void *thread_func(void *arg) {
    printf("Hello from thread!\n");
    return NULL;
}

int main() {
    pthread_t tid;
    pthread_create(&tid, NULL, thread_func, NULL);
    pthread_join(tid, NULL); // wait for thread to finish
    return 0;
}
```

Compile with:

```bash
gcc -o program program.c -lpthread
```

### Creating Processes (fork)

```c
#include <unistd.h>
#include <stdio.h>

int main() {
    pid_t pid = fork();
    
    if (pid == 0) {
        // Child process
        printf("Child PID: %d\n", getpid());
    } else {
        // Parent process
        printf("Parent PID: %d, Child PID: %d\n", getpid(), pid);
        wait(NULL); // wait for child to finish
    }
    return 0;
}
```

### Race Condition (TOCTOU)

A **TOCTOU (Time of Check to Time of Use)** race condition occurs when a program checks a condition and then uses a resource, but the resource changes between the check and the use.

```c
// Vulnerable code
if (access("file.txt", W_OK) == 0) {    // CHECK
    // Attacker swaps file.txt to /etc/passwd here
    open("file.txt", O_WRONLY);          // USE
}
```

An attacker can exploit this to write to privileged files by racing the window between check and use.

### Mutex (Mutual Exclusion)

Mutexes prevent race conditions by allowing only one thread to access a resource at a time:

```c
pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void increment() {
    pthread_mutex_lock(&lock);
    counter++;  // protected critical section
    pthread_mutex_unlock(&lock);
}
```

### Inter-Process Communication (IPC)

Processes cannot share memory directly. They communicate via:
- **Pipes**: One-way data channel (`|` in shell)
- **Named Pipes (FIFOs)**: Pipe with a filesystem name
- **Shared Memory**: `mmap()` or `shmget()` — fastest IPC
- **Sockets**: Network or Unix domain sockets
- **Signals**: Asynchronous notifications (`SIGTERM`, `SIGKILL`)

```bash
# Inspect process memory maps
cat /proc/<pid>/maps

# List threads in a process
ls /proc/<pid>/task/

# Send signal to process
kill -9 <pid>
```

## Resources

- [Linux Man Pages — pthreads(7)](https://man7.org/linux/man-pages/man7/pthreads.7.html)
- [OSDev Wiki — Processes and Threads](https://wiki.osdev.org/Processes_and_Threads)
- [CWE-362 — Race Condition](https://cwe.mitre.org/data/definitions/362.html)
- [TryHackMe — Linux Internals](https://tryhackme.com/)
- [Beej's Guide to Unix IPC](https://beej.us/guide/bgipc/)
