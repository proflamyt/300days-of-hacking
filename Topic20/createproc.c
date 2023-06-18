/*

Startup a process of your choosing, and print out some values like the PID, TID and handles for the subsequent processes/threads.

Then, have it wait for the process or thread to finish using an API like WaitForSingleObject() before closing the handles to your thread and process, using an API like CloseHandle()

*/

#include <stdio.h>
#include <windows.h>


STARTUPINFO si = {0};
PROCESS_INFORMATION pi = {0};

void handleError(char *errormesage, int status);

int main() {

    int proc = CreateProcessW(
        L"C:\\Windows\\System32\\calc.exe", NULL, NULL, NULL, FALSE, 
        BELOW_NORMAL_PRIORITY_CLASS, NULL, NULL, 
        &si, &pi );

    if (!proc) 
        handleError("process not created", GetLastError());

    printf("[+] Process created with ID %i, Handle: 0x%x \n", pi.dwProcessId, pi.hProcess);
    printf("\t[+] Process created with Thread ID %i, Handle: 0x%x", pi.dwThreadId, pi.hThread);


    WaitForSingleObject(pi.hThread, INFINITE);

    printf("(+) finished! exiting...");

    CloseHandle(pi.hThread);
    CloseHandle(pi.hProcess);
    return EXIT_SUCCESS;

    

}

void handleError(char *errormesage, int status){
    printf("[-] %s, %i", errormesage, status);
    exit(status);
}