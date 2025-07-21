# include <windows.h>

BOOL WINAPI DllMain( HINSTANCE hinstDLL, DWORD Reason, LPVOID lpvReserved )  {
    // Perform actions based on the reason for calling.
    switch( Reason ) 
    { 
        case DLL_PROCESS_ATTACH:
            MessageBoxW(NULL, L"Hacked", L"YOU HAVE BEEN", MB_ICONQUESTION | MB_OK);
            break;
    
    }
    return TRUE; 
}