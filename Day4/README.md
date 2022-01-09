# PRIVILEGE ESCALATION
## INTRODUCTION
  ### SUDO
  
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
