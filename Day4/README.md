# PRIVILEGE ESCALATION (LINUX)
Most times, when you gain a remote shell access it's very unlikely you gain access into the system as a privilege user. youd probably gain acess as a low level user.
As a low level user , what you can do on the system is restricted (this is for a good security reason). your access to certain sensive files are restricted , there are limits to what changes you can make, what you can install, generally a user like that is only given access to just what he needs to perform his important tasks and nothing more ,on rare occations, that he needs privilege access like accessing sensitive files e.t.c hed have to meet a more privilege user for this. Think of this as a comapany hirarchy , there's the lowest user , who has a boss that has a boss, where the highest boss (we know him as root here) can do anything.Then there is you a very low privilege access user in a corner office , whose job is just write a document or something, with little or no say in the workings of the company, you cant sign a document , no access to the companies files or any other files except your own. this is who we will gain access as most times ,but does that mean it's useless ? . after all there is little this low level privilege user can do . No, This is where privilege escalation comes in , we look for a vulnerabily or misconfiguration to gain access as a more privilege user or as the main boss.There are diffrent ways be can go about this , i'll take you through some manual enumeration and exploitation and update this as time goes by. but there are tools like linPeas that handles automatic enumerations for you , do well to check it out .
## INTRODUCTION
  ### SUDO
   Remember the highest boss we mentioned earlier? the one who has access to everything, thats the **root** user allowing him to handle everything in the hypothetical company can be very risky. as a root user , you can create any file, install , delete and modify them even. so you have to be very careful with this privileged power! files you install and modify can cause damages , mistakes can happen , also there are miniature tasks that are way bellow the boss that its not necessary for him to use his privilege to handle. in this case, SUDO was introduced. Sudo stands for SuperUser DO and is used to access restricted files and operations. Think of sudo as a staff of office , it let's you execute a command temporarily as another a **super user** who belongs to the sudoer group. in some cases it allows you to execute command even as the root user itself
  
  ### SETUID
    using the file owner’s privilege.
  
  ### SGID
  
  ### KERNEL
  
  ### PATH 
    in Linux is an environmental variable that tells the operating system where to search for executables
  
  

## ENUMERATION
  ### Check For Listening Ports
    netstat -lt ( tcp ports )
    netstat -s: list network usage statistics by protocol
  ### Find files with the SUID bit Set 
    find / -perm -u=s -type f 2>/dev/null
  ### Check If User Can Execute Specific Commands With Root privilege
    sudo -l
  <https://gtfobins.github.io/>
  ### Check Kernel Version
    uname -r
  
  ### List Files that have SUID or SGID bits set.
    find / -type f -perm -04000 -ls 2>/dev/null

  ### getcap tool to list enabled capabilities.
    getcap -r 2>/dev/null
  ### Check crontab
    cat /etc/crontab
   
 ### Check Environment PATH Variables
    echo $PATH
    
 ### Find Folders with writeable access
    find / -type d -writable -print
    find / -writable 2>/dev/null | cut -d "/" -f 2,3 | grep -v proc | sort -u
    
 ### Check For Mount With "no_root_squash" enabled
    showmount -e <IP>
