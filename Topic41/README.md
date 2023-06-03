# MALWARE DEV

### Process Injection


### DLL Injection

DLL: 


```
gcc .\randomDll.cpp --shared -o outputfile.dll
rundll32.exe .\outputfile.dll,DllMain
```