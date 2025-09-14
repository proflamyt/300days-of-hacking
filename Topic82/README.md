# LLDB


Dissasemble main

```
disas -n main
```

set reg x0 to 0x100e98060
```
register write x0 0x100e98060
```


```
image dump sections
```

set value 0x16f9c7a6c to 0x31337
```
memory write --size 4 0x16f9c7a6c 0x31337

```

```
expr *(int*)0x16f9c7a6c = 0x31337
```
