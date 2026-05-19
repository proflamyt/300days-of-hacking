---
title: "macOS IPC — Mach IPC"
topic: "macos-ipc"
tags: [macos, mach-ipc, ports, messages, iokit, pac, xnu, kernel]
difficulty: advanced
day: 81
layout: default
parent: Topics
nav_order: 81
---

# macOS IPC — Mach IPC

## What You Will Learn
- How Mach IPC works and what its core components are
- How to send and receive messages between processes
- How IOKit allows userspace to communicate with kernel drivers
- What PAC is and how it protects pointers on macOS/iOS

## What Is It?

**Mach IPC** is the inter-process communication mechanism at the heart of macOS and iOS (XNU kernel). It enables tasks (processes) to exchange information through ports asynchronously.

Understanding Mach IPC is essential for macOS/iOS security research, privilege escalation, and kernel exploitation.

## Core Components

| Component | Description |
|-----------|-------------|
| **Ports** | Kernel-managed communication channels, similar to pipes |
| **Port Rights** | Permissions that control how processes interact with ports |
| **Messages** | Structured data units exchanged between ports |
| **Service** | A named port registered with the bootstrap server |
| **Bootstrap Server** | `launchd` — handles service registration and discovery |

## Setting Up a Server and Client

### Process A (Server)

```c
mach_port_t server_port;

// Create port with RECEIVE right
mach_port_allocate(mach_task_self(), MACH_PORT_RIGHT_RECEIVE, &server_port);

// Add SEND right
mach_port_insert_right(mach_task_self(), server_port, server_port, MACH_MSG_TYPE_MAKE_SEND);

// Register with launchd
bootstrap_check_in(bootstrap_port, "com.example.service", server_port);
```

### Process B (Client)

```c
mach_port_t client_port;

// Look up the service
bootstrap_look_up(bootstrap_port, "com.example.service", &client_port);
```

## Mach Message Header

```c
typedef struct {
    mach_msg_bits_t     msgh_bits;         // options and port right dispositions
    mach_msg_size_t     msgh_size;         // total message size including header
    mach_port_t         msgh_remote_port;  // destination port when sending
    mach_port_t         msgh_local_port;   // reply port
    mach_port_name_t    msgh_voucher_port; // optional Mach voucher
    mach_msg_id_t       msgh_id;           // user-defined message ID
} mach_msg_header_t;
```

## Port Dispositions

A port disposition defines how the port right is passed in the message:

| Disposition | Meaning |
|-------------|---------|
| `MACH_MSG_TYPE_MOVE_SEND` | Move the send right to receiver (sender loses it) |
| `MACH_MSG_TYPE_COPY_SEND` | Copy the send right to receiver (sender keeps it) |
| `MACH_MSG_TYPE_MOVE_RECEIVE` | Move the receive right to receiver |
| `MACH_MSG_TYPE_MAKE_SEND` | Give a new send right based on a receive right the sender holds |

## Bidirectional Message — Full Example

### Get Service Port

```c
mach_port_t port;
bootstrap_look_up(bootstrap_port, "com.example.service", &port);
```

### Create Local Reply Port

```c
mach_port_t replyPort;
mach_port_allocate(task, MACH_PORT_RIGHT_RECEIVE, &replyPort);
```

### Insert Send Right on Reply Port

```c
mach_port_insert_right(task, replyPort, replyPort, MACH_MSG_TYPE_MAKE_SEND);
```

### Prepare and Send Message

```c
Message message = {0};
message.header.msgh_remote_port = port;
message.header.msgh_local_port = replyPort;

// Port dispositions
message.header.msgh_bits = MACH_MSGH_BITS_SET(
    MACH_MSG_TYPE_COPY_SEND,       // remote: send right
    MACH_MSG_TYPE_MAKE_SEND_ONCE,  // local: reply right (one-time)
    0, 0
);
```

- `MACH_MSG_TYPE_COPY_SEND`: use the send right but do not remove it from this process
- `MACH_MSG_TYPE_MAKE_SEND_ONCE`: allow receiver to reply once, then the right is destroyed

## Complex Messages

A complex Mach message can carry port descriptors in the body (in addition to the header ports):

```c
typedef struct {
    mach_msg_header_t         header;
    mach_msg_size_t           msgh_descriptor_count;
    mach_msg_port_descriptor_t descriptor;
} PortMessage;
```

### Port Descriptor (in message body)

```c
typedef struct {
    mach_port_t                 name;
    mach_msg_size_t             pad1;
    unsigned int                pad2 : 16;
    mach_msg_type_name_t        disposition : 8;
    mach_msg_descriptor_type_t  type : 8;
} mach_msg_port_descriptor_t;
```

## OOL (Out-Of-Line) Messages

OOL messages carry memory references rather than inline data:

```c
typedef struct {
    mach_msg_header_t             header;
    mach_msg_size_t               msgh_descriptor_count;
    mach_msg_ool_descriptor_t     descriptor;
} OOLMachMessage;
```

## Controlling Another Task

Two ways to control another task's memory:

1. **Target sends task port**: The target process sends a send right to its task port
2. **Privileged access**: Root + SIP allows `task_for_pid`. Requires the `com.apple.security.cs.debugger` entitlement

## Exception Ports

Any process with the right Mach port access can register as an exception handler for another process:

```c
// Allocate exception port
mach_port_allocate(mach_task_self(), MACH_PORT_RIGHT_RECEIVE, &exception_port);
mach_port_insert_right(mach_task_self(), exception_port, exception_port, MACH_MSG_TYPE_MAKE_SEND);

// Register as exception handler for this task
task_set_exception_ports(mach_task_self(), EXC_MASK_ALL, exception_port,
                         EXCEPTION_DEFAULT, THREAD_STATE_NONE);
```

## IOKit

IOKit is the framework for communicating with kernel drivers (kexts) from userspace.

```c
// Find and connect to a driver
io_service_t service = IOServiceGetMatchingService(kIOMainPortDefault,
                                                    IOServiceMatching("DriverName"));
io_connect_t connect;
IOServiceOpen(service, mach_task_self(), 1, &connect);

// Call a driver method
IOConnectCallMethod(connect, 0,  // selector
    NULL, 0, NULL, 0, NULL, NULL, NULL, NULL);

IOServiceClose(connect);
IOObjectRelease(service);
```

## PAC (Pointer Authentication Codes)

See [Topic79 — ARM64 Assembly](../Topic79/) for a detailed PAC reference.

## Resources

- [Mach IPC Security on macOS — karol-mazurek](https://karol-mazurek.medium.com/mach-ipc-security-on-macos-63ee350cb59b)
- [XNU IPC — ulexec](https://ulexec.github.io/post/2022-12-01-xnu_ipc/)
- [XNU IPC II — dmcyk.xyz](https://dmcyk.xyz/post/xnu_ipc_ii_message_apis/)
- [IOKit Documentation — Apple](https://developer.apple.com/documentation/iokit)
- [XNU Source Code](https://github.com/apple-oss-distributions/xnu)
