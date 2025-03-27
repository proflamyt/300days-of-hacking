# Heap Exploitation

### tcahe
singly linked list
mangled pointer
maximum of 7 chunks 
per thread

### Fast bins
Singly linked list with safe-linking - similar to tcache
Bin lists grow to unlimited length
Bins of constant size up to 0x80 bytes
P bit is never cleared for chunks in the fast bin
Only checks top chunk for double-free


### Unsorted Bins
Freed not fit for tchache and fast bins stays here first
On malloc if chunk is not satisfied, it gets sorted into fast or small bins
consolidates

### Small bins
Doubly linked lists
size up to 1024


### Large bins
Doubly linked lists


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
