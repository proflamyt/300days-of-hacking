# Miscellaneous


```c
void __attribute__ ((constructor)) run_before_main() {
write(1, "hello", 6);
}
```

```c
_start
 └── __libc_start_main
       └── __libc_csu_init
             └── iterate .init_array

```


```c
 __attribute__((packed)); // use exact size
```
