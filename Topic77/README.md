# Kernel Exploitation



```
proc_create
```
Create a cache with a region suitable for copying to userspace
```
kmem_cache_create
```

Allocate an object from a cache, Return pointer to the new object or NULL in case of error
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


kalloc Internal

http://www.jikos.cz/jikos/Kmalloc_Internals.html
