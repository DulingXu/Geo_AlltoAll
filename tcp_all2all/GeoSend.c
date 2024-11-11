#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>

#define MAX_HOSTS 100
#define BUFFER_SIZE 1024

void send_data_to_hosts(char *ip_addresses[], char *data) {
    int sockfd, i;
    struct sockaddr_in server_addr;
    char buffer[BUFFER_SIZE];

    // 遍历IP地址列表，直到遇到NULL
    for (i = 0; ip_addresses[i] != NULL && i < MAX_HOSTS; i++) {
        sockfd = socket(AF_INET, SOCK_STREAM, 0);
        if (sockfd < 0) {
            perror("Error creating socket");
            continue;
        }

        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(3030); // 确保端口号与服务器端一致
        if (inet_pton(AF_INET, ip_addresses[i], &server_addr.sin_addr) <= 0) {
            perror("Invalid IP address");
            close(sockfd);
            continue;
        }

        // 尝试连接服务器
        if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
            perror("Error connecting to server");
            close(sockfd);
            continue;
        } else {
            printf("Connected to server %s:3030\n", ip_addresses[i]);
        }

        // 发送数据包
        if (write(sockfd, data, strlen(data)) < 0) {
            perror("Error sending data");
        } else {
            printf("Data sent to server\n");
        }

        // 接收服务器响应
        int n = read(sockfd, buffer, BUFFER_SIZE - 1);
        if (n > 0) {
            buffer[n] = '\0'; // 确保字符串以 '\0' 结尾
            printf("Received from %s: %s\n", ip_addresses[i], buffer);
        } else {
            printf("No response from %s\n", ip_addresses[i]);
        }

        // 关闭套接字
        close(sockfd);
    }
}

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <data> <IP1> <IP2> ... <IPn>\n", argv[0]);
        exit(EXIT_FAILURE);
    }

    char *data = argv[1];
    char **ip_addresses = &argv[2]; // IP地址列表从第三个参数开始

    send_data_to_hosts(ip_addresses, data);

    return 0;
}