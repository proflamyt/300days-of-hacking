#include <stdio.h>
#include <windows.h>
#include <TlHelp32.h>


HANDLE hSnapshot;
PROCESSENTRY32 pe;
BOOL uProcess;
int pid;

int main( int argc, char* argv[] ) {

    if (argc != 2) {
        printf("[-] Usage ./%s <processname>\n", argv[0]);
        return 0;
    }

    hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);

    if (INVALID_HANDLE_VALUE == hSnapshot) {
        printf("[-] Invalid snapshot");
        return -1;
    }

    pe.dwSize = sizeof(PROCESSENTRY32);
    uProcess = Process32First(hSnapshot, &pe);

    while(uProcess) {
        if (strcmp(argv[1], pe.szExeFile) == 0) {
            pid = pe.th32ProcessID;
            printf("[+] Process ID is %i", pid);
            return 0;
        }
        uProcess = Process32Next(hSnapshot, &pe);
    }
    printf("[+] No Process with name %s running", argv[1]);
    CloseHandle(hSnapshot);
    return 0;

}