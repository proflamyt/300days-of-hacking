# REVERSE ENGINEERING

https://0xinfection.github.io/reversing

Goal of reverse engineering is Understanding WHAT it does and HOW it does it .

## X86 Assembly 


## x86 Basic Architecture

A computer application is simply a table of machine instructions stored in memory to which the binary numbers which make up the program are unique only in the way the CPU deals with them.
The basic arcchitecture of thr computer comprises of the CPU, BUS, memory, Basic I/O

The CPU (central processing Unit) comprises the unit that executes the computer program, the BUS moves data from/to the memory and CPU for processing, the memory stores information to be processed, while the I/O devices acts as an external interface with the real world.

The CPU comprises of units that fetches and decodes instructions from memory, also  stores infomation to the memory , the CPU stores these data internally using it's registers , it also uses FLags to indicate events for execution.

In a 32 bit processor , the CPU fetches 32 bits machine instruction at a go for execution from addresses , these instructions are strored in registers which are also 32 bits in lenght

In a 32-bit Intel processor, there are several types of registers, including:

1. General-purpose registers: There are 8 general-purpose registers, each of which is 32 bits wide. These registers are used to hold data and addresses during program execution.

2. Segment registers: There are 6 segment registers, each of which is 16 bits wide. These registers are used to hold segment selectors that point to different segments of memory.

3. Control registers: There are several control registers, including the program counter (PC), the flags register, and the instruction pointer (IP). These registers are used to control program execution and to store information about the state of the processor.

4. Debug registers: There are several debug registers that are used by the processor to assist with debugging.

In total, a 32-bit Intel processor has around 20 registers, including the above mentioned general-purpose, segment, control, and debug registers.

### Proceeding

proceed on what your goal is , 

find entry point



```assembly
mov rax, [rdx]
```

Will move the value pointed to by rdx into the rax register. 

```assembly
mov [rax], rdx
```

Will move the value of the rdx register into whatever memory is pointed to by the rax register. The actual value of the rax register does not change.




```assembly
MOV RAX, qword ptr [RBP + local_18]
```


Let's assume the following:

The base pointer (RBP) contains the value 0x7FFF0000.
The variable local_18 is located 24 bytes (6 quadwords) below the base pointer.
Given these values, the instruction MOV RAX, qword ptr [RBP + local_18] can be translated into the following assembly code:

therefore
```assembly
MOV RAX, qword ptr [0x7FFF0000 + 6 * 8]
```

Simplifying the calculation:

```assembly
MOV RAX, qword ptr [0x7FFF0030]
```
This means the instruction is fetching a 64-bit (quadword) value from the memory address 0x7FFF0030 and storing it in the RAX register.


### ELF BINARY

is a common standard file format for executable files in unix system .

![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/1499d412-d85f-4f68-a0b5-1e79e1c77320)

an ELF file consists of two sections 
- ELF header :  32 bytes long starting with 4 unique bytes 0x7F followed by 0x45, 0x4c, and 0x46
- File data

  ![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/71438ea0-ad14-480b-bc49-8d3ce19e8b7e)


the ".interp" section of the ELF executable contains the location of its required loader so as to let the operating system knows which specific loader to use.

![image](https://github.com/proflamyt/300days-of-hacking/assets/53262578/a45003d9-8094-4662-85b9-f51b7f8ed2fd)

checking libraries required to run program 
```
ldd elf program
```

ld.so is usually the executable which is prepackaged with glibc that loads shared library for an elf executable during execution for the process to have access to the external function

### Tools
- GDB
- Ghidra





#### Static Analysis 
dogbolt.org

Unpacking the app and check its content 

#### Dynamic Analysis

Trying to find out what is going on in run-time 







### IDA 

Define struct process 

```
shift f1;
local types
insert

struct yarn_struct {
char buf[256];
char reg1;
char reg2;
char reg3;
char reg4;
char reg5;
}

enter


rename type to

yarn_struct 


```

convert to signed 
```
hex((-0x72) & (2**64-1))
```


reference : https://0xinfection.github.io/reversing/pages/
