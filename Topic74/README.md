# Paging 

Virtual Memory addressing 




### 32 bits paging 




### 64v bits paging


512 entries per level

page table base register:    cr3 register (physical address of PGD)


### PML4 Walking

Page Global Directory (PGD) -> Page Upper Directory (PUD) -> Page Middle Directory (PMD) -> Page Table (PT)


Page Table : the final physical address of the page associated with the virtual address 

```
p/x $cr3 & ~0xfff
```


Steps :

PGD + (PGD offset) ->  

Getting PUD from bits  (12 to 51)








