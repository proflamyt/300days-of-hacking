#include <Windows.h>
#include <stdio.h>
#include <iostream>

int main()
{
    HMODULE hModule = LoadLibrary(L"user32.dll");

    if (!hModule) {
        std::cerr << "Failed To Load User32 DLL" << std::endl;
        return 1;
    }

    typedef int(WINAPI* MsgBox)(HWND, LPCSTR, LPCSTR, UINT);
    
    MsgBox OrdinalBoxA = (MsgBox)GetProcAddress(hModule, (LPCSTR)2152);

    if (!OrdinalBoxA) {
        std::cerr << "Failed To Load Function" << std::endl;
        FreeLibrary(hModule);
        return 1;
    }
    OrdinalBoxA(NULL, "hello world", "Test Message Box", MB_OK | MB_ICONINFORMATION);
    FreeLibrary(hModule);
    return 0;

}






// Run program: Ctrl + F5 or Debug > Start Without Debugging menu
// Debug program: F5 or Debug > Start Debugging menu

// Tips for Getting Started: 
//   1. Use the Solution Explorer window to add/manage files
//   2. Use the Team Explorer window to connect to source control
//   3. Use the Output window to see build output and other messages
//   4. Use the Error List window to view errors
//   5. Go to Project > Add New Item to create new code files, or Project > Add Existing Item to add existing code files to the project
//   6. In the future, to open this project again, go to File > Open > Project and select the .sln file
