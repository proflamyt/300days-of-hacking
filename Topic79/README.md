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
-> X2 * 2^3
```
lsl X3, X2, #3 
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

Note: 
stp x29, x30 saves x29 first, then x30

ldp x29, x30 loads x29 first, then x30

```asm
CBZ     x0, is_zero    ; if x0 == 0, branch to is_zero
CBNZ    x1, not_zero   ; if x1 != 0, branch to not_zero
```


### Branch (jump)

```asm
b #0x40
```
brrance to register
```asm
BR X0
```

Prologue
```asm
stp x29, x30, [sp, #-16]!
mov x29, sp 
```

Epilogue
```asm
ldp x29, x30, [sp], #16
ret
```


Project (Fibonacci in arm)


```py
def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n-1) + fibonacci(n-2)
```

```asm



  fib:
    cmp X0, #1
    b.le finish


    stp x29, x30, [sp, #-0x20]!
    mov x29, sp 


    sub X1, X0, #1
    str X1, [sp, #0x10]


    sub X2, X0, #2
    str X2, [sp, #0x18]

    mov X0, X1 // did x1
    bl fib
    str X0, [sp, #0x10]


    ldr X2,  [sp, #0x18]
    mov X0, X2
    bl fib
    
    ldr X3, [sp, #0x10]
    add X0, X3, X0


    ldp x29, x30, [sp], #0x20  

    finish:
      
      ret

```


### Equivalent X86_64 Registers 

```
RIP → PC (program counter). Not directly accessible as a general-purpose register.

RAX → X0 (first integer/return arg)

RBX → X19 (callee-saved)

RCX → X1

RDX → X2

RSP → SP (stack pointer)

RBP → X29 (frame pointer / FP)

LR (return address) → X30 (link register; holds return address after BL)
```
