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
stored in sorted order 
Each freed chunk has forward (fd) and backward (bk) pointers to link it to the next and previous chunks.


The **maximum chunk size** in glibc's heap memory allocator (`ptmalloc2`) depends on whether the chunk is allocated from the **TCache**, **Fastbin**, **Smallbin**, **Largebin**, or is handled by the **mmap system call**. 
---

### **1. TCache (Thread-local Cache) Maximum Chunk Size**
- **Maximum chunk size:** **1032 bytes** (on x86_64).
- **Why?** TCache bins store chunks up to `0x408` bytes (1032 bytes), aligned to 16 bytes.

---

### **2. Fastbin Maximum Chunk Size**
- **Maximum chunk size:** **0x80 (128 bytes)**
- **Why?** Fastbins are for quick allocations of small chunks and are limited to prevent fragmentation.

---

### **3. Smallbin Maximum Chunk Size**
- **Maximum chunk size:** **1024 bytes (0x400)**.
- **Why?** Smallbins store fixed-size allocations that avoid merging.

---

### **4. Largebin Maximum Chunk Size**
- **Maximum chunk size:** **Up to the system `mmap_threshold` (typically ~128 KB, configurable).**
- **Why?** Largebins store bigger chunks and are merged when freed.

---

### **5. mmap (Direct Memory Mapping)**
- **Threshold:** **Typically 128 KB (`MMAP_THRESHOLD`)**.
- **Why?** Chunks larger than the `mmap_threshold` bypass the heap and are allocated directly via `mmap()`.  
- **Maximum chunk size:** **Limited by available virtual memory** (theoretically **several terabytes** on 64-bit systems).

---

### **Practical Maximum Chunk Sizes (x86_64 Default)**
| Allocation Type | Max Chunk Size |
|---------------|--------------|
| **TCache** | 1032 bytes (`0x408`) |
| **Fastbin** | 128 bytes (`0x80`) |
| **Smallbin** | 1024 bytes (`0x400`) |
| **Largebin** | Up to `mmap_threshold` (~128 KB) |
| **mmap** | Several TB (limited by virtual memory) |



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
