### Mac IPC


```
// Process A (Server)
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

// Process B (Client) 
mach_port_t client_port;
bootstrap_look_up(
    bootstrap_port,                    // launchd port
    "com.example.service",             // service name
    &client_port                       // receives send right
);
```



reference: https://karol-mazurek.medium.com/mach-ipc-security-on-macos-63ee350cb59b
