# UEFI 

```
Build/OvmfX64/DEBUG_GCC5/Ovmf.map
```


A .map file is basically:

a detailed layout of how the final binary is organized in memory


.map → “where everything is placed”
.debug → “what everything means internally”


### Debugging with GDB

Get base address

```
grep PeiCore Build/OvmfX64/DEBUG_GCC5/Ovmf.map
```

Get debug offset 
```
objdump -h Build/OvmfX64/DEBUG_GCC5/X64/PeiCore.debug
```


PCI is a bus (communication system) that lets components like network cards, USB controllers, and GPUs talk to the system
