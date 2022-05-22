# Windows

Windows Internals 

Windows Architecture 

https://medium.com/@putrasulung2108/windows-architecture-d2b022f136d3


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


### Windows Architecture

##### Today, the world is more connected than ever before. Thanks to the Internet, we can communicate and share information with people and organizations around the globe in an instant. But the Internet as we know it didn’t happen overnight. In fact, the Internet has a rich architectural history.
##### Windows is the most widely used operating system in the world. It was first released in 1985 and has had several major updates since then. It has a bunch of different versions which are often called “flavors” - such as Windows 10, Windows 7, and Windows 8.1. Each version has its own unique set of features and design.
##### We all have an intuitive understanding of what an operating system is. When we think about computers, we think about operating systems. An operating system is the software that manages the computer’s hardware and provides an interface for the user to interact with the computer. Operating systems are among the most complex software in existence – they are responsible for a wide variety of tasks, ranging from managing background processes to translating human inputs into machine commands.
#####
#####
##### The Windows application programming interface (API) is the programming interface to the Microsoft Windows operating system family.  It provides services used by all Windows-based applications to enable applications to provide a Graphical User Interface (GUI), access system resources, incorporate audio and much more.  The API consists of thousands of documented, callable subroutines such as CreateProcess and CreateFile .  Major categories of Windows API functions include Base Services, Component Services, Graphics & Multimedia, Messaging, Networking and Web Services.  There are hundreds of books and websites that cover programming using the Windows API - but let me just add the disclaimer that programming using the Windows API is by no means an "entry-level" type task!  And with that, it's time to move on to Services.


##### When examining services from a programming viewpoint, a Service could refer to a callable routine in the operating system, a device driver or a server process.  However, from a user perspective, we consider a service as a process that is loaded by the OS in user-mode, independent of a logged-in user.  The Services are controlled by the Windows Service Manager.  Services can be loaded using the System account, or credentials that are assigned to that service specifically - either during the service installation, or through the properties page for that service.  Some common services include the Spooler service which controls printing, the Server service which supports file, print and named-pipe sharing over the network and the DHCP client service which registers and updates IP addresses and DNS records.

##### Windows process includes the following:

##### An executable program, consisting of initial code and data
##### A private virtual address space
##### System resources that are accessible to all threads in the process
##### A unique identifier, called a process ID
##### At least one thread of execution
##### A security context (also known as an access token.

##### The thread is what Windows schedules for execution within a process.  Without threads, the program used by the process cannot run.  Threads consist of the following components:


##### The contents of the registers representing the state of the processor
##### Two stacks - one for the thread to use when executing kernel-mode instructions, and one for user-mode
##### A private storage area used by the subsystems, run-time libraries and DLL's
##### A unique identifier, called a thread ID
