# WinDbg

 go (contine with execution)
 ```
 g
 ```

list module
```
lm
```

address func
```
x module!function
```

back trace 
```
k
```
unassemble 
```
u $entry
```
break at first assembly (bp <address or symbol name>)
```
bp $exentry
```
breakpoint unresolved func
```
bu module!function
```

disable and enable breakpoint
```
bd <addr>
be <addr>
```

list breakpoint 

```
bl
```
unassemble  function

```
uf module!function
```

unassemble 

```
u @rip
```

dump from rsp
```
dq @rsp
```
registers
```
r
```

evaluation

```
? a- b
```

trace (step instruction)
```
t
```

trace until call (stop at call)
```
tc
```

next instruction
```
p
```
go up 
```
gu
```

reload

```
.reload /f
```


modifying registers
```
 r ax = 0xf00d, rbx = 0xdeadfacebeefd00d, bl = 0x0f
```

display from address
```
db <address> L<number> == displays <number> bytes starting at <address>.

dd <address> L<number> == displays <number> doublewords (4 bytes) starting at <address>.

dq <address> L<number> == displays <number> quadwords (8 bytes) starting at <address>.

da <address> == displays as ASCII string at that address until first null terminator.
```
modifying address
```
ed rsp 0xdeadbeef
```

p command to step over a function call 
```
p 5 // step over 5 instructions and calls
```
step into
```
t 
```

go up (run until current function finishes)
```
gu
```

Reference : https://apps.p.ost2.fyi/learning/course/course-v1:OpenSecurityTraining2+Dbg1011_WinDbg1+2021_v1/block-v1:OpenSecurityTraining2+Dbg1011_WinDbg1+2021_v1+type@sequential+block@19803fcd787841369365ba76577b81a0/block-v1:OpenSecurityTraining2+Dbg1011_WinDbg1+2021_v1+type@vertical+block@7e7475bbf5b7441e953f5466535a911d
