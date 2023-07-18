# MALWARE DEV

### Process Injection


### DLL Injection

DLL: 


```
gcc .\randomDll.cpp --shared -o outputfile.dll
rundll32.exe .\outputfile.dll,DllMain
```


### DLL HIJACKING

Overwrite DLL of a legitimate process given DLL is in a writeable Location or missing

### MIC (Mandatory Integrity Control)

- Low Level : Restricted to most of the system
- Medium Level: Started by unpriviled users and administrative users if UAC is enabled
- High Level:  Running with administrative priviledge
- System Level:  Running with SYSTEM privileges


### Debugging API



### SHELLCODES



```bash

objdump -d ./example3|grep '[0-9a-f]:'|grep -v 'file'|cut \
-f2 -d:|cut -f1-6 -d' '|tr -s ' '|tr '\t' ' '| \
sed 's/ $//g'|sed 's/ /\\x/g'|paste -d '' -s | \
sed 's/ˆ/"/'|sed 's/$/"/g'


```


### portable executable


https://www.elastic.co/blog/ten-process-injection-techniques-technical-survey-common-and-trending-process