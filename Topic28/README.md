# Windows And Networking 

## INTRODUCTION TO WINDOWS


Useful Classes for enumeration 

- win32_OperatingSystem 
- win32_Bios
- win32_Service
- win32_Process

```powershell
Get-WmiObject -Class <class> 
```


### Windows Directory structure

- Perflogs : Windows Perfomance logs
- Program Files: Installed program files 
- Program Files (x86): holds 64bits program files on 64bit machine
- ProgramData
- Users 
- Default
- Windows: majority of the files required for windows os
- System, System32, SysWOW64 : Contains DLL for core windows features
- WinSxS


# Windows File System

Majourly 

- FAT32
- NTFS


#### The icacls utility

List and Manage NTFS permissions on a specific directory 

Inherit Directory permissions
- (I) : Permission Inherited from parent container
- (OI) : Object inherit : This folder and files
- (CI) : Container Inherit : This folder and subfolder
- (IO): Inherit Only : ACE does not apply to current folder
- (NP): Do not propergate inherit

Combines as

- (OI)(CI): This folder, files and subfolders
- (CI)(IO): Subfolders Only
- (OI)(IO): Files Only
- (OI)(CI)(IO): files and subfolders only

File Permissions

- (F) : full access
- (D): Delete access
- (N): No access
- (M): Modify access
- (RX): Read and execute access
- (R): Read-only
- (W): write-only


Usage: 

List permissions 

```powershell
icacls <directory>
```
# Remove permissions
```powershell
icacls <directory> /remove <user>:<permission>
```

# Grant permissions
```powershell
icacls <directory> /grant <user>:<permission>
```

### Windows Servce

query service
```powershell
sc qc <servicename>
```
stop service
```cmd
sc  stop <servicename>
```
cconfigure serviec

```cmd
sc configure <servicename> <configuration>
```


### Windows Users
The  built-in Administrator account is not the most powerful account in Windows . If you want to find something in Windows like root is for Linux, it would be the SYSTEM user account

#### Service accounts 

- LocalService (granted limited fuctionalities): NT AUTHORITY\LocalService
- NetworkService (can establish authenticated sessions for some network services ): NT AUTHORITY\NetworkService
- LocalSysten (highest level priviledge) : NT AUTHORITY\SYSTEM



### Windows Session

- Interactive Session: 
- Non-interactive Session : account has no password associated to it

### Windows WMI
used for :
- Code execution
- Scheduling process
- Setting up logging
- Managing user and group permissions
- modifying and setting system properties



```cmd
wmic os list brief
```

```powershell
Get-WmiObject -Class Win32_OperatingSystem 
```


### Windows Security Identifier
These are unique ID stored in the security databse that windows uses to identify users on a system,


### Windows SAM
The Security Account Manager is a registry file on windows  that stores local user's account passwords hash. The file is stored on your system drive at C:\WINDOWS\system32\config. However, it is not accessible (it cannot be moved nor copied) from within the Windows OS since Windows keeps an exclusive lock on the SAM file and that lock will not be released until the computer has been shut down.

### Windows UAC


### Windows Registry

Types of values :

- REG_BINARY: Binary
- REG_DWORD: 32 bit
- REG_DWORD_LITTLE_ENDIAN: 32 bit little endian
- REG_DWORD_BIG_ENDIAN: 32 bit big endian
- REG_EXPAND_AZ: null terminated string, reference to unexpanded env variables
- REG_LINK: null terminated string, symlink
- REG_NONE: none
- REG_QWORD: 64 bits
- REG_QWORD_LITTLE ENDIAN: 64 bits little endian
- REG_SZ: null terminated string, unicode or ansi


```powershell
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\Run
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\RunOnce
HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\RunOnce
```

### Windows API

These are application programming interface by microsoft that allows user applications to interact with operating system.

These APIs are basically seperated into various groups as follows:

- System Services
- Multimedia
- Networking
- User Interface
- Window Registry


Evading Maleare Detection

- syscalls 
- use of ordinals
- Hooks
- iat patching


### Windows Rights/Privileges

Rights deal with permission to access object such as files
Privileges grant user permission to perform an action such as run a program





### IAT (Import Address Table)

Contains the list of DLLs and function names and the function addresses , a P.E depends on to run

### SMB shares 

Server Message Block (SMB) is a networking protocol that allows file share and storage among users, it uses a client-server relationship. it has a default port of 445; a user can remotely access a file storage even though they are not in the physical location of the server;\
it has anonymous as well as password protected authentication

The SMB protocol will allow your team members to use these shared files as if they were on their own hard drives. 

### Kerberos Authentication


### NetNTLM Authentication



#### Extracting password hashes

```
reg save hklm\sam %tmp%/sam.reg
```


#### Priviledge Escallation Using Psexec 

Download Psexec from windows pstools

```
psexec -sid cmd.exe

```




reference : ss64.com/nt/icacls.html
