# Windows

Windows Internals 

Windows Architecture 

user mode 
manages process on behalf of user ...lower privilege

kernel mode : components where the core process of the application run

Windows Registry : collection of databases that contain systems configuration data

the registry or Windows Registry contains information, settings, options, and other values for programs and hardware installed on all versions of Microsoft Windows operating systems. For example, when a program is installed, a new subkey containing settings such as a program's location, its version, and how to start the program, are all added to the Windows Registry.
Wikipedia 


Key values
HKEY_ CURRENT_USER. Configurations info for the currently logged on user
HKEY_HKEY_USER : active user profiles on the computer
HKEY_LOCAL_MACHINE : config info of the computer
HKEY_CLASSES_ROOT : Windows uses this section to manage file type associations
HKEY_CURRENT_CONFIG : contains info about hardware profile at startup 

Process 

Threads 


Permissions and what could go wrong 

Named pipes | name squatting 

Insecure service configuration : 
Registry Key not set , user can create and allow program to run with privilege of service 

Unquoted service image path :  things the rest after space is an argument to the executable 

Dll loading: 



Windows has two command-line shells: the Command shell and PowerShell. Each shell is a software program that provides direct communication between you and the operating system or application, providing an environment to automate IT operations.


In Windows NT operating systems, a Windows service is a computer program that operates in the background.[1] It is similar in concept to a Unix daemon.[1]

a service is any Windows application that is implemented with the services API and handles low-level tasks that require little or no user interaction.







## Start Application On Boot 
Press Windows key + R.
In the run box, type regedit, and press enter.
Paste the following path in the address bar: Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run.
Right click on run and create new string value 
Edit the name to what you want and modify the value data to program path ypu want to run on boot


### Windows Services


Process 

Threads 


 
