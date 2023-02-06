# Containerization

containerisation platforms make use of the “namespace” feature of the operating sysrem kernel, which is a feature used so that processes can access resources of the operating system without being able to interact with other processes (other running application on operating system) .

Every process running on Linux will be assigned two things:

1. A namespace
2. A process identifier (PID)


### Namespace

A namespace is a kernel feature that allows user to create an isolated environment on a linux system. applications running within a namespace is unaware of other processes outside it's namespace. namespaces are important in situations where users of system wants to execute untrusted code on a machine without compromising the host Operating system.

#### Types of namespaces
In the current stable Linux Kernel version 5.7 there are seven different namespaces:

1. PID namespace: isolation of the system process tree;
2. NET namespace: isolation of the host network stack;
3. MNT namespace: isolation of host filesystem mount points;
4. UTS namespace: isolation of hostname;
5. IPC namespace: isolation for interprocess communication utilities (shared segments, semaphores);
6. USER namespace: isolation of system users IDs;
7. CGROUP namespace: isolation of the virtual cgroup filesystem of the host.

### Cgroups (control groups)
cgroups are also linux kernel features that allows you to allocate computer resources to groups of processes


### Creating NameSpace
The unshare command

```
unshare  -ipf --mount-proc # -p (create PID namespace ) , -i (create IPC namespace )
```


```
ps -ef
```






















reference: https://blog.quarkslab.com/digging-into-linux-namespaces-part-
1.html#:~:text=Moreover%2C%20namespaces%20can%20provide%20even,without%20compromising%20the%20host%20OS.
