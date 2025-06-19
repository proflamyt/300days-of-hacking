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



reference: https://karol-mazurek.medium.com/mach-ipc-security-on-macos-63ee350cb59b
https://ulexec.github.io/post/2022-12-01-xnu_ipc/
