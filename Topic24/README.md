---
title: "Containerization"
topic: "containerization"
tags: [docker, containers, namespaces, cgroups, linux, isolation]
difficulty: intermediate
day: 24
layout: default
parent: Topics
nav_order: 24
---

# Containerization

## What You Will Learn
- What containerization is and how it works under the hood
- What Linux namespaces are and the types that exist
- What cgroups are and how they limit resources
- How to create an isolated environment using `unshare`
- How container security relates to penetration testing

## What Is It?

**Containerization** is a technology that lets you run applications in isolated environments called **containers**. Containers share the host operating system kernel but are isolated from each other using Linux kernel features.

Containerization platforms (like Docker) make use of the **namespace** feature of the operating system kernel — a feature used so that processes can access resources of the operating system without being able to interact with other processes.

## Why It Matters

Understanding containerization is essential because:
- Container misconfigurations are a common attack surface in cloud environments
- Container breakout (escaping a container to reach the host) is a real attack class
- Penetration testers need to know how to enumerate and escape containers
- Defenders need to know how to harden containerized deployments

## Key Concepts

Every process running on Linux is assigned two things:

1. A **namespace**
2. A **Process Identifier (PID)**

### Namespaces

A namespace is a kernel feature that allows users to create an isolated environment on a Linux system. Applications running within a namespace are unaware of other processes outside that namespace.

Namespaces are important when users of a system want to execute untrusted code on a machine without compromising the host operating system.

#### Types of Namespaces (Linux Kernel 5.7+)

| Namespace | Isolation Provided |
|-----------|-------------------|
| PID | Isolation of the system process tree |
| NET | Isolation of the host network stack |
| MNT | Isolation of host filesystem mount points |
| UTS | Isolation of hostname |
| IPC | Isolation for interprocess communication (shared segments, semaphores) |
| USER | Isolation of system user IDs |
| CGROUP | Isolation of the virtual cgroup filesystem of the host |

### Cgroups (Control Groups)

Cgroups are also Linux kernel features that allow you to allocate computer resources (CPU, memory, I/O) to groups of processes. This prevents one container from consuming all the host's resources.

## Hands-On

### Creating a Namespace with `unshare`

```bash
# Create a new PID and IPC namespace with its own proc filesystem
unshare -ipf --mount-proc

# Verify isolation — PID 1 inside the new namespace
ps -ef
```

Inside the new namespace, your shell process has PID 1, even though it has a different PID on the host. This is the foundation of how containers work.

### Docker Basics

```bash
# Run a container
docker run -it ubuntu /bin/bash

# List running containers
docker ps

# List all containers (including stopped)
docker ps -a

# Execute a command in a running container
docker exec -it <container_id> /bin/bash

# Check the namespaces of a running container
ls -la /proc/<PID>/ns/
```

### Container Breakout (Security Context)

Common container escape techniques during penetration tests:

- **Privileged containers**: A container run with `--privileged` has full access to the host kernel. Mount the host filesystem to escape.
  ```bash
  # Inside a privileged container
  mkdir /mnt/host
  mount /dev/sda1 /mnt/host
  chroot /mnt/host
  ```

- **Writable Docker socket**: If `/var/run/docker.sock` is mounted inside a container, you can create a new privileged container.
  ```bash
  docker -H unix:///var/run/docker.sock run -it --privileged --pid=host ubuntu nsenter -t 1 -m -u -i -n /bin/bash
  ```

## Resources

- [Quarkslab — Digging into Linux Namespaces](https://blog.quarkslab.com/digging-into-linux-namespaces-part-1.html)
- [TryHackMe — Docker](https://tryhackme.com/room/docker)
- [HackTricks — Docker Breakout](https://book.hacktricks.xyz/linux-hardening/privilege-escalation/docker-security/docker-breakout-privilege-escalation)
- [Docker Documentation](https://docs.docker.com/)
