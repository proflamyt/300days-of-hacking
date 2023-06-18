# Windows And Networking 

The  built-in Administrator account is not the most powerful account in Windows . If you wanted to find something in Windows like root is for Linux, it would be the SYSTEM user account
### Windows SAM
The Security Account Manager is a registry file on windows  that stores local user's account passwords hash. The file is stored on your system drive at C:\WINDOWS\system32\config. However, it is not accessible (it cannot be moved nor copied) from within the Windows OS since Windows keeps an exclusive lock on the SAM file and that lock will not be released until the computer has been shut down.


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
