# LiNUX

### Processes
Processes are the programs that are running on your machine. They are managed by the kernel, where each process will have an ID associated with it, also known as its PID. The PID increments for the order In which the process starts. I.e. the 60th process will have a PID of 60.
Any command you give to a linux machine launches a process.

## Types:
1. Background Processes ( These are programs running at the background , usually doesnt require user's interaction e.g VPN, Antivirus)
2. Forground processes (These are programs at runs plainly for you to interact with )


### Viewing Processes 
We can use the  **ps (Stands For Process Status)** command to provide a list of the running processes as our user's session and some additional information such as its status code, the session that is running it, how much usage time of the CPU it is using, and the name of the actual program or command that is being executed:
  #### Commands
      ps (shows the process running as user's sessions )
      ps aux (Shows More detailed process running as other users and machine peocess)
      ps <PID> (Show
      top (shows you real-time statistics about the processes running on your system )
      watch ps aux (watch the process every 2s)
      
### Managing Processes 
  ### Kill Process
  To End a process you can use the **kill** command, This command terminates running processes on a Linux machine.
  \n Flags:
  1. SIGTERM - Kill the process, but allow it to do some cleanup tasks beforehand
  2. SIGKILL - Kill the process - doesn't do any cleanup after the fact
  3. SIGSTOP - Stop/suspend a process
  
  #### Commands
       pidof <Process name> (Check PID of a process by using its process name e.g ( pidof zsh )
       kill <PID>
       kill -s TERM <PID> ( Send SIGTERM  to kill process)
       
  ###  Priortize Process 
   
       

  
  
 
 
### NameSpaces
    
    
### Systemctl 

























reference : https://tryhackme.com/room/linuxfundamentalspart3
