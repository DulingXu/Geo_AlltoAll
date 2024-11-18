#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define PORT 5555
#define BUFFER_SIZE 1024

int create_subscriber(const char* endpoint) {
    int sock;
    struct sockaddr_in serv_addr;

    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Socket creation error");
        return -1;
    }

    serv_addr.sin_family = AF_INET;
    serv_addr.sin_port = htons(PORT);
    serv_addr.sin_addr.s_addr = inet_addr(endpoint);

    if (connect(sock, (struct sockaddr*)&serv_addr, sizeof(serv_addr)) < 0) {
        perror("Connection failed");
        close(sock);
        return -1;
    }

    return sock;
}

int receive_message(int sock, char* buffer, size_t buffer_size) {
    int bytes_received = recv(sock, buffer, buffer_size - 1, 0);
    if (bytes_received < 0) {
        perror("Receive failed");
        return -1;
    }
    buffer[bytes_received] = '\0'; 
    return bytes_received; 
}

void destroy_subscriber(int sock) {
    close(sock);
}

int main() {
    const char* endpoint = "127.0.0.1"; 
    char buffer[BUFFER_SIZE];
    
    int sock = create_subscriber(endpoint);
    if (sock < 0) {
        return EXIT_FAILURE;
    }

    while (1) {
        int bytes_received = receive_message(sock, buffer, sizeof(buffer));
        if (bytes_received <= 0) {
            break; 
        }
        printf("Received message: %s\n", buffer);
    }

    destroy_subscriber(sock);
    return EXIT_SUCCESS;
}
