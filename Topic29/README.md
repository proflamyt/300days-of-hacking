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




### Android reverse engineering


#### Static Analysis 
dogbolt.org

Unpacking the app and check its content 

#### Dynamic Analysis

Trying to find out what is going on in run-time 





reference : https://0xinfection.github.io/reversing/pages/
