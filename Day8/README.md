---
title: "Linux Internals"
topic: "linux-internals"
tags: [linux, processes, namespaces, systemd, files, kernel]
difficulty: intermediate
day: 8
layout: default
parent: Topics
nav_order: 8
---

# Linux Internals

## What You Will Learn
- How Linux manages processes, including viewing and killing them
- What namespaces are and how they enable container isolation
- How systemd works and how to interact with it
- The different Linux file types and what they mean

## Processes

Processes are the programs that are running on your machine. They are managed by the kernel, where each process will have an ID associated with it — also known as its PID. The PID increments in the order in which processes start. For example, the 60th process will have a PID of 60.

Any command you give to a Linux machine launches a process.

## Types

1. **Background Processes**: Programs running in the background, usually without requiring user interaction (e.g., VPN, Antivirus).
2. **Foreground Processes**: Programs running plainly for you to interact with.


### Viewing Processes

We can use the **`ps` (Process Status)** command to get a list of running processes for the current user's session along with additional information such as status code, session, CPU usage time, and the name of the program being executed.

#### Commands

```bash
ps                  # show processes running in the user's session
ps aux              # show more detailed processes running as other users and machine processes
ps <PID>            # show a specific process by PID
top                 # show real-time statistics about running processes
watch ps aux        # watch the process list update every 2 seconds
```

### Managing Processes

#### Kill a Process

To end a process you can use the **`kill`** command, which terminates running processes on a Linux machine.

**Signals:**

1. `SIGTERM` — Kill the process, but allow it to do some cleanup tasks beforehand.
2. `SIGKILL` — Kill the process immediately — no cleanup.
3. `SIGSTOP` — Stop/suspend a process.

```bash
pidof <process name>       # check PID of a process by name (e.g., pidof zsh)
kill <PID>                 # send default SIGTERM
kill -s TERM <PID>         # explicitly send SIGTERM to kill process
```

### Prioritize a Process

Linux can run quite a number of processes at a time, and the OS assigns resources to each. Sometimes an unimportant process takes a considerably large amount of resources, leaving the important processes you are working with very slow. You can assign priorities to processes. This priority is called **Niceness** in Linux, and it has a value between -20 to 19. The lower the niceness index, the higher the priority given to that task.

```bash
nice -n <nice value> <process name>   # assign a nice value before starting a process
renice <nice value> -p <PID>          # re-prioritize a process using its PID
```


### Namespaces

The Operating System uses namespaces to split up the resources (such as CPU, RAM, and priority) available on the computer among processes. It is important that the resources of your machine are allocated to processes accordingly. If Firefox took up all of your machine's RAM even though it needs very little, other programs would not run unless Firefox was killed. One benefit of the operating system is that it handles these allocations behind the scenes.

Namespaces are also great for security — they isolate processes from each other. Only processes in the same namespace will be able to see each other.

When a system boots and initializes, `systemd` is one of the first processes started. Any program we want to start will begin as a **child process** of systemd — controlled by systemd, but running as its own process.

Linux namespaces are the underlying technology behind container technologies like Docker.

```bash
lsns       # list existing namespaces on your machine
ps axf     # show process tree with parent-child relationships
```

### Systemd / Systemctl

`systemd` is a suite of basic building blocks for a Linux system. It provides a system and service manager that runs as PID 1 and starts the rest of the system processes.

```bash
pstree      # show running processes as a tree
```

`systemctl`: This command allows us to interact with the systemd process.

```bash
systemctl start <service>     # start a service
systemctl stop <service>      # stop a service
systemctl status <service>    # check the status of a service
systemctl enable <service>    # enable a service to start on boot
```


## Files

Linux represents almost everything as a file. The first character in an `ls -l` listing tells you what type of file it is:

- `-` is a regular file
- `d` is a directory (directories are actually just special files!)
- `l` is a symbolic link (a file that transparently points to another file or directory)
- `p` is a named pipe (also known as a FIFO)
- `c` is a character device file (backed by a hardware device that produces or receives data streams, such as a microphone)
- `b` is a block device file (backed by a hardware device that stores and loads blocks of data, such as a hard drive)
- `s` is a Unix socket (essentially a local network connection encapsulated in a file)


**References:**

- Linux Room: https://tryhackme.com/room/linuxfundamentalspart3
- Demystifying namespaces and containers in Linux: https://opensource.com/article/19/10/namespaces-and-containers-linux
