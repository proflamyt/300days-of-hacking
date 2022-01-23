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
      $ ps (shows the process running as user's sessions )
      $ ps aux (Shows More detailed process running as other users and machine peocess)
      $ ps <PID> (Show
      $ top (shows you real-time statistics about the processes running on your system )
      $ watch ps aux (watch the process every 2s)
      
### Managing Processes 
  ### Kill Process
  To End a process you can use the **kill** command, This command terminates running processes on a Linux machine.
  
  
  Flags:
  1. SIGTERM - Kill the process, but allow it to do some cleanup tasks beforehand
  2. SIGKILL - Kill the process - doesn't do any cleanup after the fact
  3. SIGSTOP - Stop/suspend a process
  
  #### Commands
       $ pidof <Process name> (Check PID of a process by using its process name e.g ( pidof zsh )
       $ kill <PID>
       $ kill -s TERM <PID> ( Send SIGTERM  to kill process)
       
  ###  Priortize Process 
 Linux can run quite a number of processes at a time, these resources are assigned resources by the OS. there are times unimportant process takes considerably large amount of resource , leaving the important process you are working with very slow. you can assign priorities to your processes as per your requirements.This priority is called Niceness in Linux, and it has a value between -20 to 19. The lower the Niceness index, the higher would be a priority given to that task.
 #### Commands
      $ nice -n <Nice value> <process name> ( assign nice value before starting a process) 
      $ renice <Nice Value> -p <PID> ( To repriotize a process using its process ID)
     
 
### NameSpaces
 The Operating System (OS) uses namespaces to ultimately split up the resources (such as CPU, RAM and priority) available on the computer to  processes.It is impoortant that the resources of your machine are allocated to your processes accordingly.If you were to start firefox for instance and it takes up all your machine's RAM even though the firefox needs very little of this , the other programs wont run unless the firefox process is killed.this can disrupt your day to day usage of your machine . one of the benefits of operating system is it does these allocations for us behind the scene , this way, each program you start gets their share of the resource available on your machine without you explicitly bothering  to allocate them yourself.
 Namespaces are also great for security as it is a way of isolating processes from another -- only those that are in the same namespace will be able to see each other.
 
 For example, once a system boots and it initialises, systemd is one of the first processes that are started. Any program or piece of software that we want to start will start as what's known as a child process of systemd. This means that it is controlled by systemd, but will run as its own process (although sharing the resources from systemd) to make it easier for us to identify and the likes.
Linux namespaces are the underlying tech behind container technologies like Docker.

    $ lsns ( list existing namespaces on your machine ) 
    $ ps axf
    
### Systemd / Systemctl 
systemd is a suite of basic building blocks for a Linux system. It provides a system and service manager that runs as PID 1 and starts the rest of the system proceses.

    $ pstree () (The pstree command shows running processes as a tree)

systemctl : This command allows us to interact with the systemd process

























**Reference :** 

linux Room https://tryhackme.com/room/linuxfundamentalspart3

Demystifying namespaces and containers in Linux https://opensource.com/article/19/10/namespaces-and-containers-linux
