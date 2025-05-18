# ARM 

 Register 64-bit X register (X0..X30), or as a 32-bit W register (W0..W30).# ARM 

### mov instruction

```asm
  mov x1, #0xbeef
  movk x1, #0xdead, lsl 16
  result : 0xdeadbeef
```


### mul instruction

```asm
  mul X1, X0, X1
  result : X1 = X0 * X1
```

### add instruction

```asm
add X0, X1, X2
# X0 = X1 + X2
```

### MADD instruction
multiply 2 regs,  adds a third register value, and writes the result to the destination register

```asm
 madd X3, X0, X1, X2
 X3 = X2 + (X0 * X1) 
```

### Unsigned divide

```asm
udiv X2, X0, X1
```

### MSUB instruction
multiply 2 regs, and subtract 3rd value

```asm
 msub X3, X0, X1, X2
 X3 =  X2 - (X0 * X1) 
```

### can you get modulus?

```
5/2

remainder?

5 - (2 * 2)

dividend - (res * divisor )

remainder 1
```

### lsl instruction shift left 

```asm
lsl reg1, reg1, reg2
result : reg1 = reg1 << reg2
```

### lsr instruction shift left 

```asm
lsr reg1, reg1, reg2
result : reg1 = reg1 >> reg2
```


### ldr instruction load from memory to register

```asm
ldr x0, [x1]
result: goes into memory pointed to by X1 fetch content and put into X0
> can compute offset by
ldr x0, [x1, #8]
result : memory pointed to by X1 + 8
```

### str instruction stores from register to memory

```asm
str x0, [x1]
result: goes into memory pointed to by X1 put what is in X0
> can compute offset
str X4, [X3, #0x10]
store into memory pointed to by X3+ 0x10 X4
```


### stp instruction
store 2 registers at once 

```asm
  stp X0, X1, [X3]
  result: stores X0 into memory pointed to by X3 and X1 into next 8 bytes  
```

### ldp instruction
Loads two 64-bit registers from memory.

```asm
  ldp X0, X1, [X3]
  result: load into X0 into memory pointed to by X3 and into X1 memory pointed to by the next 8 bytes  
```

pop 2 instruction from the stack
```asm
  ldp X1, X2, [sp], #16
```

push on the stack

```asm
str X0, [sp, #-8]!
```
Remember Stack grows "down" memory, that is it grows by reducing in mordern architecture

 > Pre-indexing: [SP, #-16]! – updates the base register before accessing memory.
 
 > Post-indexing: [SP], #16 – accesses memory, then updates the base register.
 
 > Offset: [SP, #offset] – accesses memory at the address SP + offset


