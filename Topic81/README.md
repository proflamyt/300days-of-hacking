### Mac IPC

Mach IPC
It enables tasks (processes) to exchange information through ports asynchronously. Main components:

- Ports: Kernel-managed communication channels, similar to pipes.

- Port Rights: Permissions that control how processes can interact with ports (via handles).

- Messages: Structured data units exchanged between ports.

- Service: A named port registered with the bootstrap server.

- Bootstrap Server: A service (typically launchd) responsible for service registration and discovery.

```c
// Process A (Server/ Task with recieve right, attach send right to port for bootstrap) 
mach_port_t server_port;

// Create port with RECEIVE right
kern_return_t kr = mach_port_allocate(
    mach_task_self(),                  // our task
    MACH_PORT_RIGHT_RECEIVE,           // want receive right
    &server_port                       // port name to create
);

// Create SEND right
mach_port_insert_right(
    mach_task_self(),                  // our task
    server_port,                       // port
    server_port,                       // same port 
    MACH_MSG_TYPE_MAKE_SEND            // convert to send right
);

// Register with launchd
bootstrap_check_in(
    bootstrap_port,                    // launchd port
    "com.example.service",             // service name
    server_port                        // port with send right
);

// Process B (Client/ Task that obtains send right from bootstrap) 
mach_port_t client_port;
bootstrap_look_up(
    bootstrap_port,                    // launchd port
    "com.example.service",             // service name
    &client_port                       // receives send right
);
```

# MAC Message Header 

```
typedef struct {
  mach_msg_bits_t       msgh_bits;
  mach_msg_size_t       msgh_size;
  mach_port_t           msgh_remote_port;
  mach_port_t           msgh_local_port;
  mach_port_name_t      msgh_voucher_port;
  mach_msg_id_t         msgh_id;
} mach_msg_header_t;
```



A brief description of these fields is the following:
- msgh_bits - options and message metadata, such as disposition of port rights in the message
- msgh_size - total message size, including header
- msgh_remote_port - remote Mach port, used as the destination when sending a message, or a reply port when receiving
- msgh_local_port - local Mach port, the port the message was received on, or a reply port when sending a message
- msgh_voucher_port - port identifying a Mach Voucher, that’s an optional field
- msgh_id - user defined message identifier


📦 What is a Port Disposition?
A port disposition defines how the port right is passed or interpreted in the message.

Examples of dispositions include:

| Disposition                  | Meaning                                                         |
| ---------------------------- | --------------------------------------------------------------- |
| `MACH_MSG_TYPE_MOVE_SEND`    | Move the *send right* to the receiver (sender loses it)         |
| `MACH_MSG_TYPE_COPY_SEND`    | Copy the *send right* to the receiver (sender keeps it too)     |
| `MACH_MSG_TYPE_MOVE_RECEIVE` | Move the *receive right* to the receiver                        |
| `MACH_MSG_TYPE_MAKE_SEND`    | Give a new send right based on a receive right the sender holds |



# Bidirectional Message 

### get service port 
```
mach_port_t port;
if (bootstrap_look_up(bootstrapPort, <service name>", &port) !=
  KERN_SUCCESS) {
  return EXIT_FAILURE;
}
```


### Create Local port  (with receive right)

```
mach_port_t replyPort;
if (mach_port_allocate(task, MACH_PORT_RIGHT_RECEIVE, &replyPort) !=
    KERN_SUCCESS) {
  return EXIT_FAILURE;
}
```

### Insert send right 

```
if (mach_port_insert_right(
        task, replyPort, replyPort, MACH_MSG_TYPE_MAKE_SEND) !=
    KERN_SUCCESS) {
  return EXIT_FAILURE;
}
```

### Prepare Message to send 

```
Message message = {0};
message.header.msgh_remote_port = port;
message.header.msgh_local_port = replyPort;
```

### Create Port Disposition

how the port rights are transferred
```
message.header.msgh_bits = MACH_MSGH_BITS_SET(
    /* remote */ MACH_MSG_TYPE_COPY_SEND,
    /* local */ MACH_MSG_TYPE_MAKE_SEND_ONCE,
    /* voucher */ 0,
    /* other */ 0);
```

MACH_MSG_TYPE_COPY_SEND tells the kernel:

“Use this send right to deliver the message, but do not remove it from my process.”

MACH_MSG_TYPE_MAKE_SEND_ONCE tells the kernel:

"allow the receiver to send only one reply message, after which the right is destroyed".

# Complex Message

complex Mach message:

```
typedef struct {
  mach_msg_header_t header;
  mach_msg_size_t msgh_descriptor_count;
  mach_msg_port_descriptor_t descriptor;
} PortMessage;
```
### port descriptors 
Unlike msgh_remote_port and msgh_local_port, which are part of the message header, port descriptors live inside the body of a message — and they allow you to send additional ports along with the message.

```
typedef struct{
  mach_port_t                   name;
  mach_msg_size_t               pad1;
  unsigned int                  pad2 : 16;
  mach_msg_type_name_t          disposition : 8;
  mach_msg_descriptor_type_t    type : 8;
} mach_msg_port_descriptor_t;
```


```c
typedef struct {
    mach_msg_type_descriptor_t  type;
    mach_port_t                 name;
    mach_msg_type_name_t        disposition;
} mach_msg_port_descriptor_t;
```

# OOL Messages


```
typedef struct {
  mach_msg_header_t header;
  mach_msg_size_t msgh_descriptor_count;
  mach_msg_ool_descriptor_t descriptor;
} OOLMachMessage;
```

```
typedef struct{
  void*                         address;
  mach_msg_size_t               size;
  boolean_t                     deallocate: 8;
  mach_msg_copy_options_t       copy: 8;
  unsigned int                  pad1: 8;
  mach_msg_descriptor_type_t    type: 8;
} mach_msg_ool_descriptor_t;

```


### Controlling Another Task On MacOs/IOS

1. **The target process sends its task port to the other process** :
        A task must send another task a send right (MACH_PORT_RIGHT_SEND) to its task port. With that, the other task can call mach_vm_write() on it.

2. **The other process obtains the task port by privilege (root / entitlement)** :
         If the caller is root and System Integrity Protection (SIP) allows it, Or if the process has the com.apple.security.cs.debugger entitlement (task_for_pid-allow)
   




reference: 
- https://karol-mazurek.medium.com/mach-ipc-security-on-macos-63ee350cb59b

- https://ulexec.github.io/post/2022-12-01-xnu_ipc/
- https://dmcyk.xyz/post/xnu_ipc_ii_message_apis/xnu_ipc_ii_message_apis/
