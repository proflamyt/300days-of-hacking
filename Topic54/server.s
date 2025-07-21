.intel_syntax noprefix
.globl _start

.section .text

_start:


    # Create socket 
    mov rax, 41
    mov rdi, 2
    mov rsi, 1
    mov rdx, 0
    syscall

    # Bind Socket to port and address

    mov r9, rax
    mov rdi, r9
    mov rax, 49;
    mov rsi, OFFSET soc_addr; # address of
    mov rdx, 16
    syscall
    

    # Listen On socket port
    mov rdi, r9;
    mov rsi, 0;
    mov rax, 50;
    syscall

    

server:

    #  accept connection on socket with an address and port 

    mov rdi, r9;
    mov rsi, 0;
    mov rdx, 0
    mov rax, 43
    syscall



    # r9 = socketfd, r8=newsocfd

    mov r8, rax; # move socket fd to r8

    # Fork

    mov rax, 57;
    syscall



    cmp rax, 0x0;
    jne tidy_up; # parent


    # Close file descriptor to Listen
    
    mov rdi, r9; # r9 is free
    mov rax, 3
    syscall


    # Read from socket fd

    mov r10, r8; # r8 free
    mov rsi, OFFSET request
    mov rdx, 256;
    mov rdi, r10;
    mov rax, 0;
    syscall
    

    # get  request

    mov r12, OFFSET request
    mov r14, r12

    # save file lenght (check)
    mov r8, rax
 

    # Extract File name

extract_file:
    cmp byte ptr [r12], 0x20;
    je find_endfile
    inc r12;
    jmp extract_file;


find_endfile:
    mov byte ptr [r12], 0x00;
    inc r12
    mov r11, r12;
    jmp endfile

   
    # Create endfile
endfile:
    cmp byte ptr [r11], 0x20
    je check_method
    inc r11
    jmp endfile

check_method:
    mov rsi, OFFSET method       
    mov rdi, r14        
    mov ecx, 4            
    repe cmpsb  
    je post_handle
    jmp open_pfile   


    # Open file

open_pfile:
    mov byte ptr [r11], 0x0
    mov rsi, 0
    mov rdi, r12 
    mov rax, 2;
    syscall



    # Read the file
    mov r13, rax
    mov rsi, OFFSET file_content
    mov rdx, 1024;
    mov rdi, rax;
    mov rax, 0;
    syscall

    # Close the file 
    mov r14, rax
    mov rdi, r13;
    mov rax, 3
    syscall


    # Write to socket fd 

    mov rsi, OFFSET response;
    mov rdx, 19 
    mov rdi, r10
    mov rax, 1
    syscall


    # Write to file content to socket fd 

    mov rsi, OFFSET file_content;
    mov rdx, r14 
    mov rdi, r10
    mov rax, 1
    syscall

    # Close connection


    
    

    # Exit
exit:
    mov rdi, r10;
    mov rax, 3;
    syscall
    
    mov rdi, 0
    mov rax, 60     # SYS_exit
    syscall

    jmp server;

     

tidy_up:
   
    mov rdi, r8;
    mov rax, 3
    syscall

    jmp server



post_handle:


    open_file:
        xor rsi, rsi
        xor rdx, rdx
        mov byte ptr [r11], 0x0
        mov rsi, 0001
        or rsi, 0100
        mov edx, 0777
        mov rdi, r12 
        mov rax, 2;
        syscall


    mov r9, OFFSET request;
    mov rcx, 0;

    get_content:

        cmp dword ptr [r9], 0x0a0d0a0d;
        je extract_body
        inc rcx;
        inc r9;
        jmp get_content;


    extract_body:

        add rcx, 4
        add r9, 4
        sub r8, rcx;  #r9 is content-lenght


        # write to file
        mov r14, rax
        mov rsi, r9;
        mov rdx,  r8; 
        mov rdi, rax
        mov rax, 1
        syscall

        # close file

        mov rdi, r14;
        mov rax, 3
        syscall

        # Write to Socket

        mov rsi, OFFSET response;
        mov rdx, 19 
        mov rdi, r10
        mov rax, 1
        syscall


        # exit
        jmp exit



 
.section .data

response:
    .asciz "HTTP/1.0 200 OK\r\n\r\n"


method:
    .asciz "POST"
     

soc_addr:
    .word 2
    .word 0x5000
    .text 0x0


.section .bss  

request:
  .space 256

file_content:
    .space 1024

