Process Injection

Before we dig into process injection, let us try to understand what is a process, an application and a service.
Application

An application is a program with which we interact on the desktop. This is where we spend most of us spend our time on a desktop or a laptop. Google Chrome, MS Word, iTunes, Skype - these are all applications.
Service

A service is a process which runs in the background and does not interact with the desktop. There are some services which run before the user has even logged in.

Services can be viewed through Task Manager  Open Services.

Under the “Startup Type” value, they are classified as follows:

    Automatic:These are started at boot time
    Automatic Delayed: Services that are started after almost everything else has powered up
    Manual:These are started either by a user or specific circumstances.
    Disabled:These services should not be run at all.
    
Process

A process is an instance of a particular executable (.exe program file) running. A given application may have several processes running simultaneously. For example, all major browsers such as google chrome, Firefox run several processes at once, with each tab, utility and extension is actually being a separate instance/process of the same executable. 
Each process has its own private virtual memory space also known as sandbox that is isolated from other processes. Inside this memory space, you can find the process executable; its list of loaded modules (DLLs or shared libraries); and its stacks, heaps, and allocated memory regions containing everything from user input to application-specific data structures (such as SQL tables, Internet history logs, and configuration files).

Handle 

An handle is an integer value that identifies a thread/registry/files/process to Windows. handles should be released after use, just like free after malloc . If you do not release your handle to a resource fter use (use CloseHandle()), other people may not be able to access it - this is why you sometimes cannot delete a file because Windows claims it is in use. 

_EPROCESS is the name of the structure that Windows uses to represent a process. Below image shows the basic process resources. SIDs (security identifiers) are used by the kernel to enforce security and access control.

Process Injection (also known as Code Injection)

Some antimalware defences rely on process names to detect malwares in a system. Hence, adversaries started injecting code into processes in order to evade these types of defences.

Process injection is a method of executing arbitrary code in the address space of a separate live process. Running code in the context of another process may allow access to the process's memory, system/network resources, and possibly elevated privileges.

But there are various legitimate uses for process injection as well. For Ex: debuggers use this method to hook into applications and allow developers to troubleshoot their programs. Antivirus programs often inject code into web browsers. They can use it to monitor network traffic and block dangerous web content.
Processes Targeted by Adversaries for Process Injection

Windows processes that are commonly used by threat actors are as follows:

    Processes of common software including iexplore.exe, ieuser.exe, opera.exe, chrome.exe, firefox.exe and outlook.exe
    Built-in native Windows processes including explorer.exe, svchost.exe, regsvr32.exe, dllhost.exe, services.exe, cvtres.exe,msbuild.exe, RegAsm.exe, RegSvcs.exe, rundll32.exe, arp.exe, PowerShell.exe, vbc.exe, csc.exe, AppLaunch.exe and cmd.exe

DLL Injection technique is one of the majorly used process injection technique.
What are DLL files?

A Dynamic Link Library (DLL) file is a file containing a library of functions and data. It facilitates code reuse as many programs can do common tasks by simply loading a DLL and call its functions
Process Injection Techniques

As per Mitre there are 11 process injections techniques for windows, Linux and MacOS but we will only discuss 4 techniques.

CLASSIC DLL INJECTION VIA CREATEREMOTETHREAD AND LOADLIBRARY: the malware writes the path to its malicious dynamic-link library (DLL) in the virtual address space of another process, and ensures the remote process loads it by creating a remote thread in the target process.

Remote DLL injection: A malicious process forces the target process to load a specified DLL from disk by calling LoadLibrary or the native LdrLoadDll. (Note: the DLL must exist on disk of the victim system prior to being injected).

LoadLibrary is a function that loads the specified module into the address space of the calling process. The specified module may cause other modules to be loaded.

PE Injection: A Portable Execution (PE) is a Windows file format for executable code. It is a data structure containing all the information required so that Windows knows how to execute it. Here the malware injects a malicious PE image into an already running process. This is a disk-less operation, i.e. the malware does not need to write its payload onto disk prior to the injection.

Reflective DLL injection: A malicious process writes a DLL (as a sequence of bytes) into the memory space of a target process. The DLL handles its own initialization without the help of the Windows loader. The DLL does not need to exist on disk prior to being injected.

Hollow process injection: A malicious adversary can start a new instance of a legitimate process, such as lsass.exe. Before the process’ first thread begins, the malware frees the memory containing the lsass.exe code and replaces it with the body (payload) of the malware. In this sense, it executes only malicious code for the remainder of the process’ lifetime.





https://www.elastic.co/blog/ten-process-injection-techniques-technical-survey-common-and-trending-process