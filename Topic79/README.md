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

```
 madd X3, X0, X1, X2
 X3 = (X0 * X1) + X2
```
