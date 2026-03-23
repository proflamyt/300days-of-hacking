# Format String

```
rdi, rsi, rdx, rcx, r8, r9, [rsp], [rsp+8], [rsp+0x10]
```


You have access to read and write to the stack

To write arbitrary value to any location, you can write the value to stack then write to that particular address



```
a%25$n
```
count the len of stuff before % , go to the 25 arg and put the len as 4 bytes 
