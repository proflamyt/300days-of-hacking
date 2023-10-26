# Building Server (ASM)


### How Socket communicate

For two computers to communicate over network, both nodes needs to specify the mode at which they want to send and receive the data. One of the nodes need to listen, while the other connects.
The node that listens is called a server, while that that connects is called the client.

#### Socket creation Process


```plaintext

 ----------------------------
 |        socket             |
  ----------------------------
              |
              |
 ----------------------------
 |           bind            |
  ----------------------------
              |
              |
 ----------------------------
 |        listen             |
  ----------------------------
              |
              |
  ---------------------------
 |        accept             |
  ----------------------------
              |
              |
 ----------------------------
 |        read/write         |
 -----------------------------


```

```c
int socket (
int domain,
type,
protocol
)
```


