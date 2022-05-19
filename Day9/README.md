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


 
