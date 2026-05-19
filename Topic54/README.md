---
title: "Building a Web Server in Assembly"
topic: "building-web-server-asm"
tags: [assembly, sockets, c, networking, linux, syscalls, low-level]
difficulty: advanced
day: 54
layout: default
parent: Topics
nav_order: 54
---

# Building a Web Server in Assembly

## What You Will Learn
- How socket communication works at the system call level
- The sequence of C socket API calls to create a server
- How to map C socket functions to Linux syscalls
- Why this knowledge is valuable for exploit development

## What Is It?

Building a web server from scratch — using sockets in C or directly in assembly — teaches you exactly how network communication works at the lowest level. This knowledge is fundamental for exploit development, writing shellcode that connects back, and understanding network programs.

## Why It Matters

- Shellcode for reverse shells uses these exact syscalls
- Understanding socket code helps you read and modify exploits
- Binary analysis of network programs requires knowing the socket API
- CTF challenges often involve writing custom network clients

## How Sockets Communicate

For two computers to communicate over a network, both nodes need to specify how they will send and receive data. One node listens (the server) while the other connects (the client).

The server-side socket creation process:

```plaintext
socket()
   |
bind()
   |
listen()
   |
accept()
   |
read()/write()
```

## Socket API in C

### Creating a Socket

```c
int socket(int domain, int type, int protocol);
```

Example:

```c
int sfd = socket(AF_INET, SOCK_STREAM, 0);
// AF_INET = IPv4, SOCK_STREAM = TCP, 0 = default protocol
```

### Binding the Socket

```c
struct sockaddr_in my_addr;
my_addr.sin_family = AF_INET;
my_addr.sin_port   = htons(8080);
my_addr.sin_addr.s_addr = INADDR_ANY;

bind(sfd, (struct sockaddr *)&my_addr, sizeof(my_addr));
```

The `sockaddr_in` structure:

```c
struct sockaddr_in {
    sa_family_t    sin_family;   // address family: AF_INET
    in_port_t      sin_port;     // port in network byte order
    struct in_addr sin_addr;     // internet address
};
```

### Listening for Connections

```c
int listen(int sockfd, int backlog);
// backlog = max number of pending connections in the queue
```

### Accepting a Connection

```c
struct sockaddr_in client_addr;
socklen_t client_len = sizeof(client_addr);

int conn_fd = accept(sfd, (struct sockaddr *)&client_addr, &client_len);
```

### Reading and Writing

```c
char buf[1024];
int n = read(conn_fd, buf, sizeof(buf));
write(conn_fd, "HTTP/1.1 200 OK\r\n\r\nHello!", 25);
close(conn_fd);
```

### Complete Minimal HTTP Server

```c
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <netinet/in.h>

int main() {
    int sfd = socket(AF_INET, SOCK_STREAM, 0);

    struct sockaddr_in addr = {0};
    addr.sin_family      = AF_INET;
    addr.sin_port        = htons(8080);
    addr.sin_addr.s_addr = INADDR_ANY;

    bind(sfd, (struct sockaddr *)&addr, sizeof(addr));
    listen(sfd, 5);

    while (1) {
        int conn = accept(sfd, NULL, NULL);
        char buf[4096];
        read(conn, buf, sizeof(buf));

        char response[] = "HTTP/1.1 200 OK\r\nContent-Length: 13\r\n\r\nHello, World!";
        write(conn, response, sizeof(response));
        close(conn);
    }
    return 0;
}
```

## Linux Syscall Numbers for Sockets

On x86-64 Linux, socket operations map to syscall number 41:

```
socket   = 41
bind     = 49
listen   = 50
accept   = 43
connect  = 42
send     = 44
recv     = 45
close    = 3
```

Reference: [Linux x86-64 System Call Table](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)

### Socket Syscall in Assembly

```asm
; socket(AF_INET=2, SOCK_STREAM=1, 0) = sockfd
mov rax, 41         ; sys_socket
mov rdi, 2          ; AF_INET
mov rsi, 1          ; SOCK_STREAM
mov rdx, 0          ; protocol
syscall
```

## Resources

- [Beej's Guide to Network Programming](https://beej.us/guide/bgnet/)
- [Linux System Call Table](https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/)
- [OSDev — Network Stack](https://wiki.osdev.org/Network_Stack)
- [Low-Level Programming — Igor Zhirkov](https://nostarch.com/lowlevel)
