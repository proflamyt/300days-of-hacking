# Exploit Development

## Display information about the used memory regions in a program or a process 

### Static Analysis (program)

```bash
$ file <binary> # Display generic information about a file
$ checksec <binary> # Check binary security
$ readelf <binary> # Display Information about elf obj file
$ objdump -M Intel -d <binary> # Decompile program 
```

### Dynamic Analysis (Process)

Using GDB

```bash
$ gdb -q <binary>
        $ disas <function> # disassemble funtion
        $ b *<function> # break at function
        $ r # run
        $ info registers # To display the registers 0xf7fc1000
        $ i r <register> # Display info about a particular register
        $ x/16dx $esp # eXamines 16 elements of type Double (4 bytes) and displays it as heX number starting from memory address in register $esp

```


Global Variable

.data section : .data contains static initialized data 


file offset 