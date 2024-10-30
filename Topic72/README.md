# Heap Exploitation

### Use After Free (Tcache)

```c
a = malloc(128);
free(a);
scanf("%d", a);
password_pointer = malloc(128)
printf("%s", password_pointer)
```


### Double Free

corrupt next in tcache

```
a = malloc(128);
free(a);
a[1]= 1234
free(a)
```
