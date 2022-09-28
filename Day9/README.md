# Windows

Windows Internals 

Windows Architecture 

https://medium.com/@putrasulung2108/windows-architecture-d2b022f136d3

# TERMs
## Windows API
An Application Programming Interface Provided by microsoft for interaction with windows operating system. 

## DLL (Dynamic Linker Library)
A DLL is a library that contains code and data that can be used by more than one program at the same time.

## windows SDK (Software Development Kit)
 Header files that expose exported DLL functions to the Programmer
 
## Windows.h
Include all the basic windows SDK you need in a typical basic windows application

## user mode 
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






Windows Vista, Windows Server 2003, Windows XP, Windows 2000 and Windows NT are all part of the Windows NT family ( NT-based) of Microsoft operating systems. They are all preemptive, reentrant operating systems, which have been designed to work with either uniprocessor- or symmetrical multi processor (SMP)-based Intel x86 computers. To process input/output (I/O) requests it uses packet-driven I/O which utilises I/O request packets (IRPs) and asynchronous I/O. Starting with Windows XP, Microsoft began building in 64-bit support into their operating systems — before this their operating systems were based on a 32-bit model. The architecture of Windows NT is highly modular, and consists of two main layers: a user mode and a kernel mode. Programs and subsystems in user mode are limited in terms of what system resources they have access to, while the kernel mode has unrestricted access to the system memory and external devices. The kernels of the operating systems in this line are all known as hybrid kernels - although it is worth noting that this term is disputed, with the claim that the kernel is essentially a monolithic kernel that is structured somewhat like a microkernel. The architecture is comprised of a hybrid kernel, Hardware Abstraction Layer (HAL), drivers, and Executive, which all exist in kernel mode . The higher-level services are implemented by the executive.

User mode in the Windows NT line is made of subsystems capable of passing I/O requests to the appropriate kernel mode software drivers by using the I/O manager. Two subsystems make up the user mode layer of Windows 2000: the Environment subsystem (runs applications written for many different types of operating systems), and the Integral subsystem (operates system specific functions on behalf of the environment subsystem). Kernel mode in Windows 2000 has full access to the hardware and system resources of the computer. The kernel mode stops user mode services and applications from accessing critical areas of the operating system that they should not have access to.

The Executive interfaces with all the user mode subsystems. It deals with I/O, object management, security and process management. The kernel sits between the Hardware Abstraction Layer and the Executive to provide multiprocessor synchronization, thread and interrupt scheduling and dispatching, and trap handling and exception dispatching. The kernel is also responsible for initialising device drivers at bootup. Kernel mode drivers exist in three levels: highest level drivers, intermediate drivers and low level drivers. Windows Driver Model (WDM) exists in the intermediate layer and was mainly designed to be binary and source compatible between Windows 98 and Windows 2000. The lowest level drivers are either legacy Windows NT device drivers that control a device directly or can be a PnP hardware bus.

User mode

The user mode is made up of subsystems which can pass I/O requests to the appropriate kernel mode drivers via the I/O manager (which exists in kernel mode). Two subsystems make up the user mode layer of Windows 2000: the Environment subsystem and the Integral subsystem.

The environment subsystem was designed to run applications written for many different types of operating systems. None of the environment subsystems can directly access hardware, and must request access to memory resources through the Virtual Memory Manager that runs in kernel mode. Also, applications run at a lower priority than kernel mode processes. Currently, there are three main environment subsystems: the Win32 subsystem, an OS/2 subsystem and a POSIX subsystem.

The Win32 environment subsystem can run 32-bit Windows applications. It contains the console as well as text window support, shutdown and hard-error handling for all other environment subsystems. It also supports Virtual DOS Machines (VDMs), which allow MS-DOS and 16-bit Windows 3.x ( Win16) applications to run on Windows. There is a specific MS-DOS VDM which runs in its own address space and which emulates an Intel 80486 running MS-DOS 5. Win16 programs, however, run in a Win16 VDM. Each program, by default, runs in the same process, thus using the same address space, and the Win16 VDM gives each program its own thread to run on. However, Windows 2000 does allow users to run a Win16 program in a separate Win16 VDM, which allows the program to be preemptively multitasked as Windows 2000 will pre-empt the whole VDM process, which only contains one running application. The OS/2 environment subsystem supports 16-bit character-based OS/2 applications and emulates OS/2 1.x, but not 32-bit or graphical OS/2 applications as used with OS/2 2.x or later. The POSIX environment subsystem supports applications that are strictly written to either the POSIX.1 standard or the related ISO/ IEC standards.

The integral subsystem looks after operating system specific functions on behalf of the environment subsystem. It consists of a security subsystem, a workstation service and a server service. The security subsystem deals with security tokens, grants or denies access to user accounts based on resource permissions, handles logon requests and initiates logon authentication, and determines which system resources need to be audited by Windows 2000. It also looks after Active Directory. The workstation service is an API to the network redirector, which provides the computer access to the network. The server service is an API that allows the computer to provide network services.

Kernel mode

Windows 2000 kernel mode has full access to the hardware and system resources of the computer and runs code in a protected memory area. It controls access to scheduling, thread prioritisation, memory management and the interaction with hardware. The kernel mode stops user mode services and applications from accessing critical areas of the operating system that they should not have access to as user mode processes ask the kernel mode to perform such operations on its behalf.

Kernel mode consists of executive services, which is itself made up on many modules that do specific tasks, kernel drivers, a kernel and a Hardware Abstraction Layer, or HAL.

Executive

The Executive interfaces with all the user mode subsystems. It deals with I/O, object management, security and process management. It contains various components, including the I/O Manager, the Security Reference Monitor, the Object Manager, the IPC Manager, the Virtual Memory Manager (VMM), a PnP Manager and Power Manager, as well as a Window Manager which works in conjunction with the Windows Graphics Device Interface (GDI). Each of these components exports a kernel-only support routine allows other components to communicate with one another. Grouped together, the components can be called executive services. No executive component has access to the internal routines of any other executive component.

The object manager is a special executive subsystem that all other executive subsystems must pass through to gain access to Windows 2000 resources — essentially making it a resource management infrastructure service. The object manager is used to reduce the duplication of object resource management functionality in other executive subsystems, which could potentially lead to bugs and make development of Windows 2000 harder . To the object manager, each resource is an object, whether that resource is a physical resource (such as a file system or peripheral) or a logical resource (such as a file). Each object has a structure or object type that the object manager must know about. When another executive subsystem requests the creation of an object, they send that request to the object manager which creates an empty object structure which the requesting executive subsystem then fills in . Object types define the object procedures and any data specific to the object. In this way, the object manager allows Windows 2000 to be an object oriented operating system, as object types can be thought of as classes that define objects.

Each instance of an object that is created stores its name, parameters that are passed to the object creation function, security attributes and a pointer to its object type. The object also contains an object close procedure and a reference count to tell the object manager how many other objects in the system reference that object and thereby determines whether the object can be destroyed when a close request is sent to it . Every object exists in a hierarchical object namespace.

Further executive subsystems are the following:

 I/O Manager: allows devices to communicate with user-mode subsystems. It translates user-mode read and write commands in read or write IRPs which it passes to device drivers. It accepts file system I/O requests and translates them into device specific calls, and can incorporate low-level device drivers that directly manipulate hardware to either read input or write output. It also includes a cache manager to improve disk performance by caching read requests and write to the disk in the background
    Security Reference Monitor (SRM): the primary authority for enforcing the security rules of the security integral subsystem . It determines whether an object or resource can be accessed, via the use of access control lists (ACLs), which are themselves made up of access control entries (ACEs). ACEs contain a security identifier (SID) and a list of operations that the ACE gives a select group of trustees — a user account, group account, or logon session — permission (allow, deny, or audit) to that resource.
    IPC Manager: short for Interprocess Communication Manager, this manages the communication between clients (the environment subsystem) and servers (components of the Executive). It can use two facilities: the Local Procedure Call (LPC) facility (clients and servers on the one computer) and the Remote Procedure Call (RPC) facility (where clients and servers are situated on different computers. Microsoft has had significant security issues with the RPC facility .
    Virtual Memory Manager: manages virtual memory, allowing Windows 2000 to use the hard disk as a primary storage device (although strictly speaking it is secondary storage). It controls the paging of memory in and out of physical memory to disk storage.
    Process Manager: handles process and thread creation and termination
    PnP Manager: handles Plug and Play and supports device detection and installation at boot time. It also has the responsibility to stop and start devices on demand — sometimes this happens when a bus gains a new device and needs to have a device driver loaded to support that device. Both FireWire and USB are hot-swappable and require the services of the PnP Manager to load, stop and start devices. The PnP manager interfaces with the HAL, the rest of the executive (as necessary) and with device drivers.
    Power Manager: the power manager deals with power events and generates power IRPs. It coordinates these power events when several devices send a request to be turned off it determines the best way of doing this.
    The display system has been moved from user mode into the kernel mode as a device driver contained in the file Win32k.sys. There are two components in this device driver — the Window Manager and the GDI:
        Window Manager: responsible for drawing windows and menus. It controls the way that output is painted to the screen and handles input events (such as from the keyboard and mouse), then passes messages to the applications that need to receive this input
        GDI: the Graphics Device Interface is responsible for tasks such as drawing lines and curves, rendering fonts and handling palettes. Windows 2000 introduced native alpha blending into the GDI.

Kernel & kernel-mode drivers

The kernel sits between the HAL and the Executive and provides multiprocessor synchronization, thread and interrupt scheduling and dispatching, and trap handling and exception dispatching. The kernel often interfaces with the process manager. The kernel is also responsible for initialising device drivers at bootup that are necessary to get the operating system up and running.

Windows 2000 uses kernel-mode device drivers to enable it to interact with hardware devices. Each of the drivers has well defined system routines and internal routines that it exports to the rest of the operating system. All devices are seen by user mode code as a file object in the I/O manager, though to the I/O manager itself the devices are seen as device objects, which it defines as either file, device or driver objects. Kernel mode drivers exist in three levels: highest level drivers, intermediate drivers and low level drivers. The highest level drivers, such as file system drivers for FAT and NTFS, rely on intermediate drivers. Intermediate drivers consist of function drivers — or main driver for a device — that are optionally sandwiched between lower and higher level filter drivers. The function driver then relies on a bus driver — or a driver that services a bus controller, adapter, or bridge — which can have an optional bus filter driver that sits between itself and the function driver. Intermediate drivers rely on the lowest level drivers to function. The Windows Driver Model (WDM) exists in the intermediate layer. The lowest level drivers are either legacy Windows NT device drivers that control a device directly or can be a PnP hardware bus. These lower level drivers directly control hardware and do not rely on any other drivers..

Hardware abstraction layer

The Windows 2000 Hardware Abstraction Layer, or HAL, is a layer between the physical hardware of the computer and the rest of the operating system. It was designed to hide differences in hardware and therefore provide a consistent platform on which applications may run. The HAL includes hardware specific code that controls I/O interfaces, interrupt controllers and multiple processors.

Windows 2000 was designed to support the 64-bit DEC Alpha. After Compaq announced they would discontinue support of the processor, Microsoft stopped releasing tests build of Windows 2000 for AXP to the public, stopping with beta 3. Development of Windows on the Alpha continued internally in order to continue to have a 64-bit architecture development model ready until the wider availability of the Intel Itanium IA-64 architecture. The HAL now only supports hardware that is compatible with the Intel x86 architecture.

Paste the following path in the address bar: Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Run.
Right click on run and create new string value 
Edit the name to what you want and modify the value data to program path ypu want to run on boot


### Windows Services


Process 

Threads 



#### WINDOWS ARCHITECTURE

The Windows NT operating system family's architecture consists of two layers (user mode and kernel mode), with many different modules within both of these layers.

The architecture of Windows NT, a line of operating systems produced and sold by Microsoft, is a layered design that consists of two main components, user mode and kernel mode. It is a preemptive, reentrant multitasking operating system, which has been designed to work with uniprocessor and symmetrical multiprocessor (SMP)-based computers. To process input/output (I/O) requests, they use packet-driven I/O, which utilizes I/O request packets (IRPs) and asynchronous I/O. Starting with Windows XP, Microsoft began making 64-bit versions of Windows available; before this, there were only 32-bit versions of these operating systems.

Programs and subsystems in user mode are limited in terms of what system resources they have access to, while the kernel mode has unrestricted access to the system memory and external devices. Kernel mode in Windows NT has full access to the hardware and system resources of the computer. The Windows NT kernel is a hybrid kernel; the architecture comprises a simple kernel, hardware abstraction layer (HAL), drivers, and a range of services (collectively named Executive), which all exist in kernel mode.

User mode in Windows NT is made of subsystems capable of passing I/O requests to the appropriate kernel mode device drivers by using the I/O manager. The user mode layer of Windows NT is made up of the "Environment subsystems", which run applications written for many different types of operating systems, and the "Integral subsystem", which operates system-specific functions on behalf of environment subsystems. The kernel mode stops user mode services and applications from accessing critical areas of the operating system that they should not have access to.

The Executive interfaces, with all the user mode subsystems, deal with I/O, object management, security and process management. The kernel sits between the hardware abstraction layer and the Executive to provide multiprocessor synchronization, thread and interrupt scheduling and dispatching, and trap handling and exception dispatching. The kernel is also responsible for initializing device drivers at bootup. Kernel mode drivers exist in three levels: highest level drivers, intermediate drivers and low-level drivers. Windows Driver Model (WDM) exists in the intermediate layer and was mainly designed to be binary and source compatible between Windows 98 and Windows 2000. The lowest level drivers are either legacy Windows NT device drivers that control a device directly or can be a plug and play (PnP) hardware bus. 

# USER MODE
User mode is made up of various system-defined processes and DLLs.

The interface between user mode applications and operating system kernel functions is called an "environment subsystem." Windows NT can have more than one of these, each implementing a different API set. This mechanism was designed to support applications written for many different types of operating systeUREms. None of the environment subsystems can directly access hardware; access to hardware functions is done by calling into kernel mode routines.
There are three main environment subsystems: the Win32 subsystem, an OS/2 subsystem and a POSIX subsystem.

# Win32 environment subsystem
The Win32 environment subsystem can run 32-bit Windows applications. It contains the console as well as text window support, shutdown and hard-error handling for all other environment subsystems. It also supports Virtual DOS Machines (VDMs), which allow MS-DOS and 16-bit Windows (Win16) applications to run on Windows NT. There is a specific MS-DOS VDM that runs in its own address space and which emulates an Intel 80486 running MS-DOS 5.0. Win16 programs, however, run in a Win16 VDM. Each program, by default, runs in the same process, thus using the same address space, and the Win16 VDM gives each program its own thread on which to run. However, Windows NT does allow users to run a Win16 program in a separate Win16 VDM, which allows the program to be preemptively multitasked, as Windows NT will pre-empt the whole VDM process, which only contains one running application. The Win32 environment subsystem process (csrss.exe) also includes the window management functionality, sometimes called a "window manager". It handles input events (such as from the keyboard and mouse), then passes messages to the applications that need to receive this input. Each application is responsible for drawing or refreshing its own windows and menus, in response to these messages. 

# OS/2 environment subsystem

The OS/2 environment subsystem supports 16-bit character-based OS/2 applications and emulates OS/2 1.x, but not 32-bit or graphical OS/2 applications as used with OS/2 2.x or later, on x86 machines only.[3] To run graphical OS/2 1.x programs, the Windows NT Add-On Subsystem for Presentation Manager must be installed.[3] The last version of Windows NT to have an OS/2 subsystem was Windows 2000; it was removed as of Windows XP.

# POSIX environment subsystem
Main article: Microsoft POSIX subsystem

The POSIX environment subsystem supports applications that are strictly written to either the POSIX.1 standard or the related ISO/IEC standards. This subsystem has been replaced by Interix, which is a part of Windows Services for UNIX.[4] This was in turn replaced by the Windows Subsystem for Linux.
Security subsystem

The security subsystem deals with security tokens, grants or denies access to user accounts based on resource permissions, handles login requests and initiates login authentication, and determines which system resources need to be audited by Windows NT.[citation needed] It also looks after Active Directory.[citation needed] The workstation service implements the network redirector, which is the client side of Windows file and print sharing; it implements local requests to remote files and printers by "redirecting" them to the appropriate servers on the network.[6] Conversely, the server service allows other computers on the network to access file shares and shared printers offered by the local system.[7]
Kernel mode

Windows NT kernel mode has full access to the hardware and system resources of the computer and runs code in a protected memory area.[8] It controls access to scheduling, thread prioritization, memory management and the interaction with hardware. The kernel mode stops user mode services and applications from accessing critical areas of the operating system that they should not have access to; user mode processes must ask the kernel mode to perform such operations on their behalf.

While the x86 architecture supports four different privilege levels (numbered 0 to 3), only the two extreme privilege levels are used. Usermode programs are run with CPL 3, and the kernel runs with CPL 0. These two levels are often referred to as "ring 3" and "ring 0", respectively. Such a design decision had been done to achieve code portability to RISC platforms that only support two privilege levels,[9] though this breaks compatibility with OS/2 applications that contain I/O privilege segments that attempt to directly access hardware.[10]

Code running in kernel mode includes: the executive, which is itself made up of many modules that do specific tasks; the kernel, which provides low-level services used by the Executive; the Hardware Abstraction Layer (HAL); and kernel drivers.[8][11]
Executive

The Windows Executive services make up the low-level kernel-mode portion, and are contained in the file NTOSKRNL.EXE.[8] It deals with I/O, object management, security and process management. These are divided into several subsystems, among which are Cache Manager, Configuration Manager, I/O Manager, Local Procedure Call (LPC), Memory Manager, Object Manager, Process Structure and Security Reference Monitor (SRM). Grouped together, the components can be called Executive services (internal name Ex). System Services (internal name Nt), i.e., system calls, are implemented at this level, too, except very few that call directly into the kernel layer for better performance.[citation needed]

The term "service" in this context generally refers to a callable routine, or set of callable routines. This is distinct from the concept of a "service process", which is a user mode component somewhat analogous to a daemon in Unix-like operating systems.
Each object in Windows NT exists in a global namespace. This is a screenshot from Sysinternals WinObj.

# Object Manager
    The Object Manager (internal name Ob) is an executive subsystem that all other executive subsystems, especially system calls, must pass through to gain access to Windows NT resources—essentially making it a resource management infrastructure service.[12] The object manager is used to reduce the duplication of object resource management functionality in other executive subsystems, which could potentially lead to bugs and make development of Windows NT harder. To the object manager, each resource is an object, whether that resource is a physical resource (such as a file system or peripheral) or a logical resource (such as a file). Each object has a structure or object type that the object manager must know about.
    Object creation is a process in two phases, creation and insertion. Creation causes the allocation of an empty object and the reservation of any resources required by the object manager, such as an (optional) name in the namespace. If creation was successful, the subsystem responsible for the creation fills in the empty object. Finally, if the subsystem deems the initialization successful, it instructs the object manager to insert the object, which makes it accessible through its (optional) name or a cookie called a handle. From then on, the lifetime of the object is handled by the object manager, and it's up to the subsystem to keep the object in a working condition until being signaled by the object manager to dispose of it.
    Handles are identifiers that represent a reference to a kernel resource through an opaque value. Similarly, opening an object through its name is subject to security checks, but acting through an existing, open handle is only limited to the level of access requested when the object was opened or created.
    Object types define the object procedures and any data specific to the object. In this way, the object manager allows Windows NT to be an object-oriented operating system, as object types can be thought of as polymorphic classes that define objects. Most subsystems, though, with a notable exception in the I/O Manager, rely on the default implementation for all object type procedures.
    Each instance of an object that is created stores its name, parameters that are passed to the object creation function, security attributes and a pointer to its object type. The object also contains an object close procedure and a reference count to tell the object manager how many other objects in the system reference that object and thereby determines whether the object can be destroyed when a close request is sent to it.Every named object exists in a hierarchical object namespace.
# Cache Controller
    Closely coordinates with the Memory Manager, I/O Manager and I/O drivers to provide a common cache for regular file I/O. The Windows Cache Manager operates on file blocks (rather than device blocks), for consistent operation between local and remote files, and ensures a certain degree of coherency with memory-mapped views of files, since cache blocks are a special case of memory-mapped views and cache misses a special case of page faults.
Configuration Manager
    Implements the system calls needed by Windows Registry.
# I/O Manager
    Allows devices to communicate with user-mode subsystems. It translates user-mode read and write commands into read or write IRPs which it passes to device drivers. It accepts file system I/O requests and translates them into device specific calls, and can incorporate low-level device drivers that directly manipulate hardware to either read input or write output. It also includes a cache manager to improve disk performance by caching read requests and write to the disk in the background.
#  Procedure Call (LPC)
    Provides inter-process communication ports with connection semantics. LPC ports are used by user-mode subsystems to communicate with their clients, by Executive subsystems to communicate with user-mode subsystems, and as the basis for the local transport for Microsoft RPC.
# Memory Manager
    Manages virtual memory, controlling memory protection and the paging of memory in and out of physical memory to secondary storage, and implements a general-purpose allocator of physical memory. It also implements a parser of PE executables that lets an executable be mapped or unmapped in a single, atomic step.
    Starting from Windows NT Server 4.0, Terminal Server Edition, the memory manager implements a so-called session space, a range of kernel-mode memory that is subject to context switching just like user-mode memory. This lets multiple instances of the kernel-mode Win32 subsystem and GDI drivers run side-by-side, despite shortcomings in their initial design. Each session space is shared by several processes, collectively referred to as a "session".
    To ensure a degree of isolation between sessions without introducing a new object type, the association between processes and sessions is handled by the Security Reference Monitor, as an attribute of a security subject (token), and it can only be changed while holding special privileges.
    The relatively unsophisticated and ad hoc nature of sessions is due to the fact they weren't part of the initial design, and had to be developed, with minimal disruption to the main line, by a third party (Citrix Systems) as a prerequisite for their terminal server product for Windows NT, called WinFrame. Starting with Windows Vista, though, sessions finally became a proper aspect of the Windows architecture. No longer a memory manager construct that creeps into user mode indirectly through Win32, they were expanded into a pervasive abstraction affecting most Executive subsystems. As a matter of fact, regular use of Windows Vista always results in a multi-session environment
# Process Structure
    Handles process and thread creation and termination, and it implements the concept of Job, a group of processes that can be terminated as a whole, or be placed under shared restrictions (such a total maximum of allocated memory, or CPU time). Job objects were introduced in Windows 2000.
# PnP Manager
    Handles plug and play and supports device detection and installation at boot time. It also has the responsibility to stop and start devices on demand—this can happen when a bus (such as USB or IEEE 1394 FireWire) gains a new device and needs to have a device driver loaded to support it. Its bulk is actually implemented in user mode, in the Plug and Play Service, which handles the often complex tasks of installing the appropriate drivers, notifying services and applications of the arrival of new devices, and displaying GUI to the user.
# Power Manager
    Deals with power events (power-off, stand-by, hibernate, etc.) and notifies affected drivers with special IRPs (Power IRPs).
#Security Reference Monitor (SRM)
    The primary authority for enforcing the security rules of the security integral subsystem. It determines whether an object or resource can be accessed, via the use of access control lists (ACLs), which are themselves made up of access control entries (ACEs). ACEs contain a Security Identifier (SID) and a list of operations that the ACE gives a select group of trustees—a user account, group account, or login session—permission (allow, deny, or audit) to that resource.
# GDI
    The Graphics Device Interface is responsible for tasks such as drawing lines and curves, rendering fonts and handling palettes. The Windows NT 3.x series of releases had placed the GDI component in the user-mode Client/Server Runtime Subsystem, but this was moved into kernel mode with Windows NT 4.0 to improve graphics performance.

# Kernel

The kernel sits between the HAL and the Executive and provides multiprocessor synchronization, thread and interrupt scheduling and dispatching, and trap handling and exception dispatching; it is also responsible for initializing device drivers at bootup that are necessary to get the operating system up and running. That is, the kernel performs almost all the tasks of a traditional microkernel; the strict distinction between Executive and Kernel is the most prominent remnant of the original microkernel design, and historical design documentation consistently refers to the kernel component as "the microkernel".

The kernel often interfaces with the process manager. The level of abstraction is such that the kernel never calls into the process manager, only the other way around (save for a handful of corner cases, still never to the point of a functional dependence).
Hybrid kernel design

The Windows NT design includes many of the same objectives as Mach, the archetypal microkernel system, one of the most important being its structure as a collection of modules that communicate via well-known interfaces, with a small microkernel limited to core functions such as first-level interrupt handling, thread scheduling and synchronization primitives. This allows for the possibility of using either direct procedure calls or interprocess communication (IPC) to communicate between modules, and hence for the potential location of modules in different address spaces (for example in either kernel space or server processes). Other design goals shared with Mach included support for diverse architectures, a kernel with abstractions general enough to allow multiple operating system personalities to be implemented on top of it and an object-oriented organisation.

The primary operating system personality on Windows is the Windows API, which is always present. The emulation subsystem which implements the Windows personality is called the Client/Server Runtime Subsystem (csrss.exe). On versions of NT prior to 4.0, this subsystem process also contained the window manager, graphics device interface and graphics device drivers. For performance reasons, however, in version 4.0 and later, these modules (which are often implemented in user mode even on monolithic systems, especially those designed without internal graphics support) run as a kernel-mode subsystem.

Applications that run on NT are written to one of the OS personalities (usually the Windows API), and not to the native NT API for which documentation is not publicly available (with the exception of routines used in device driver development). An OS personality is implemented via a set of user-mode DLLs (see Dynamic-link library), which are mapped into application processes' address spaces as required, together with an emulation subsystem server process (as described previously). Applications access system services by calling into the OS personality DLLs mapped into their address spaces, which in turn call into the NT run-time library (ntdll.dll), also mapped into the process address space. The NT run-time library services these requests by trapping into kernel mode to either call kernel-mode Executive routines or make Local Procedure Calls (LPCs) to the appropriate user-mode subsystem server processes, which in turn use the NT API to communicate with application processes, the kernel-mode subsystems and each other.
Kernel-mode drivers

Windows NT uses kernel-mode device drivers to enable it to interact with hardware devices. Each of the drivers has well defined system routines and internal routines that it exports to the rest of the operating system. All devices are seen by user mode code as a file object in the I/O manager, though to the I/O manager itself the devices are seen as device objects, which it defines as either file, device or driver objects. Kernel mode drivers exist in three levels: highest level drivers, intermediate drivers and low level drivers. The highest level drivers, such as file system drivers for FAT and NTFS, rely on intermediate drivers. Intermediate drivers consist of function drivers—or main driver for a device—that are optionally sandwiched between lower and higher level filter drivers. The function driver then relies on a bus driver—or a driver that services a bus controller, adapter, or bridge—which can have an optional bus filter driver that sits between itself and the function driver. Intermediate drivers rely on the lowest level drivers to function. The Windows Driver Model (WDM) exists in the intermediate layer. The lowest level drivers are either legacy Windows NT device drivers that control a device directly or can be a PnP hardware bus. These lower level drivers directly control hardware and do not rely on any other drivers.
Hardware abstraction layer

The Windows NT hardware abstraction layer (HAL) is a layer between the physical hardware of the computer and the rest of the operating system. It was designed to hide differences in hardware and provide a consistent platform on which the kernel is run. The HAL includes hardware-specific code that controls I/O interfaces, interrupt controllers and multiple processors.

However, despite its purpose and designated place within the architecture, the HAL isn't a layer that sits entirely below the kernel, the way the kernel sits below the Executive: All known HAL implementations depend in some measure on the kernel, or even the Executive. In practice, this means that kernel and HAL variants come in matching sets that are specifically constructed to work together.

In particular hardware abstraction does not involve abstracting the instruction set, which generally falls under the wider concept of portability. Abstracting the instruction set, when necessary (such as for handling the several revisions to the x86 instruction set, or emulating a missing math coprocessor), is performed by the kernel, or via hardware virtualization. 
=======
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
>>>>>>> 83cd668d44fc0d8a9c6fad6c0dd38f6a56012c2d
