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




https://infosecwriteups.com/the-toddlers-introduction-to-heap-exploitation-part-1-515b3621e0e8

https://infosecwriteups.com/the-toddlers-introduction-to-heap-exploitation-part-2-d1f325b74286
