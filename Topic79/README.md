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
