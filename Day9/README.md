# Windows

Windows Internals 

Windows Registry : collection of databases that contain systems configuration data
Key values
HKEY_ CURRENT_USER. Configurations info for the currently logged on user
HKEY_HKEY_USER : active user profiles on the computer
HKEY_LOCAL_MACHINE : config info of the computer
HKEY_CLASSES_ROOT
HKEY_CURRENT_CONFIG : contains info about hardware profile at startup 

## Start Application On Boot 
Press Windows key + R.
In the run box, type regedit, and press enter.
Paste the following path in the address bar: Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run.
Right click on run and create new string value 
Edit the name to what you want and modify the value data to program path ypu want to run on boot


### Windows Services


Process 

Threads 


Permissions and what could go wrong 

Named pipes | name squatting 

Insecure service configuration : 
Registry Key not set , user can create and allow program to run with privilege of service 

Unquoted service image path :  things the rest after space is an argument to the executable 

Dll loading: 
