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
creating socket

```c
int socket (
int domain,
type,
protocol
)
```

Binding Socket

```c
bind(
sfd,
(struct sockaddr_in *) &my_addr,
sizeof(my_addr);
)
```


```c
struct sockaddr_in {
sa_family_t sa_family;
in_port_t sin_port
char sa_data[14]
}
```
Listening

```c
int listen (
int sockfd,
int backlog
)
```


# Accepting 

```c
accept (
int sockfd,
(struct sockaddr_in *) &my_addr,
sizeof(my_addr);
)
```











references: https://blog.rchapman.org/posts/Linux_System_Call_Table_for_x86_64/
