# Kernel Exploitation



```
proc_create
```
Create a cache with a region suitable for copying to userspace
```
kmem_cache_create
```

Allocate an object from a specific  cache, Return pointer to the new object or NULL in case of error
```
 kmem_cache_alloc
```

to copy the pointed-to data from user space into kernel space 
```
copy_from_user
unsigned long copy_from_user(void *to, const void __user *from, unsigned long n);
```

Kernel space to user space
```
copy_to_user
unsigned long copy_to_user(void __user *to, const void *from, unsigned long n);
```

```
sudo cat /proc/slabinfo
```


Kernel Heap

caches are backed backed by pages , unique by sizes , 

e.g a cache of specifically of size 512, may contain diffrent slabs each with 8 objects as each slab is backed by a page . (512*8 == a 4kb page)


Kernel Heap Hardnening 

-> SLUB allocation randomization

-> Hardened Usercopy

-> freelist hardening : Mangling Next pointer : rev(ptr) ^ ptr_addr ^ random


FreeList randomization

When allocating objects from slabs , the slots are returned randomly

Free list poisoning
Overwrite next pointer such that when next it is allocated it returns your address

####  SMAP, SMEP, and 



KASLR 

randomize base address during boot




kalloc Internal

http://www.jikos.cz/jikos/Kmalloc_Internals.html
