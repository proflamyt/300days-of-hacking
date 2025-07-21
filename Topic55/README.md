# GNU DEBUGGER


### Commands 

0x5654a77a6e41138d

```
$ echo "set disassembly-flavor intel" >> ~/.gdbinit


# start program and stop at _start
starti

# run a program normally without breakpoint

run | r

# continue program execution

continue | c

# print/ $register

p/x $rdi (print hex in register rdi)

# dissassemble portion in memory

disass *main

# Examine memory

x/amountType $register #(example : x/gx $rbp-0x18 examine 8bytes in memory address rbp-0x18)

# Step Over Instruction

si # step one intruction at a time
ni # step one intruction at a time and over function call

# Display

display/8i $rip # Display next 8 instructions

display/4gx $rsp # Display 4 8byte hex values from rsp 

# Information
info proc map
info break
info frame

dis break 2
```

cast 0 to file ptr and get offset to read_ptr
```
 p &((struct _IO_FILE *)0)->_IO_read_ptr
```
cast to file ptr plus
```
 p *(struct _IO_FILE_plus *) fp
```


Analysing Programs with setuid set


1. copy program to location with permission
2. set base address if you havent
   ```
   nano ~/.gdbinit

        set $BASE = 0x0000555555554000
   ```
