.intel_syntax noprefix
.globl _start

.section .text

_start:

    mov rax, 41
    mov rdi, 2
    mov rsi, 1
    mov rdx, 0
    syscall

    mov rdi, rax
    mov rax, 49;
    mov rsi, OFFSET soc_addr
    mov rdx, 16
    syscall
    

    mov rdi, 0
    mov rax, 60     # SYS_exit
    syscall


.section .data

soc_addr:
    .word 2
    .word 0x5000
    .text 0x0
