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
        server_addr.sin_port = htons(8080);
        if (inet_pton(AF_INET, ip_addresses[i], &server_addr.sin_addr) <= 0) {
            perror("Invalid IP address");
            close(sockfd);
            continue;
        }

        if (connect(sockfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) < 0) {
            perror("Error connecting to server");
            close(sockfd);
            continue;
        }

        // 发送数据包
        write(sockfd, data, strlen(data));
        read(sockfd, buffer, BUFFER_SIZE);
        printf("Received from %s: %s\n", ip_addresses[i], buffer);

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

// int main(int argc, char *argv[]) {
//     int num_hosts;
//     char *data = "Hello from the client!";

//     // 检查命令行参数个数
//     if (argc < 2) {
//         printf("Usage: %s <IP address 1> <IP address 2> ... <IP address N>\n", argv[0]);
//         return 1;
//     }

//     // 调用发送数据的函数
//     num_hosts = argc - 1;
//     send_data_to_hosts(num_hosts, argv + 1, data);

//     return 0;
// }




// #include <stdio.h>
// #include <stdlib.h>
// #include <string.h>
// #include <unistd.h>
// #include <sys/types.h>
// #include <sys/socket.h>
// #include <netinet/in.h>
// #include <arpa/inet.h>

// #define MAX_HOSTS 100
// #define BUFFER_SIZE 1024

// void send_data_to_hosts(int num_hosts, char *ip_addresses[], char *data) {
//     int sockfd, i;
//     struct sockaddr_in server_addr[MAX_HOSTS];
//     char buffer[BUFFER_SIZE];

//     // 创建并连接 TCP 套接字
//     for (i = 0; i < num_hosts; i++) {
//         sockfd = socket(AF_INET, SOCK_STREAM, 0);
//         if (sockfd < 0) {
//             perror("Error creating socket");
//             return;
//         }

//         server_addr[i].sin_family = AF_INET;
//         server_addr[i].sin_port = htons(8080);
//         if (inet_pton(AF_INET, ip_addresses[i], &server_addr[i].sin_addr) <= 0) {
//             perror("Invalid IP address");
//             close(sockfd);
//             return;
//         }

//         if (connect(sockfd, (struct sockaddr *)&server_addr[i], sizeof(server_addr[i])) < 0) {
//             perror("Error connecting to server");
//             close(sockfd);
//             return;
//         }

//         // 发送数据包
//         write(sockfd, data, strlen(data));
//         read(sockfd, buffer, BUFFER_SIZE);
//         printf("Received from %s: %s\n", ip_addresses[i], buffer);

//         // 关闭套接字
//         close(sockfd);
//     }
// }

// int main(int argc, char *argv[]) {
//     int num_hosts;
//     char *data = "Hello from the client!";

//     // 检查命令行参数个数
//     if (argc < 2) {
//         printf("Usage: %s <IP address 1> <IP address 2> ... <IP address N>\n", argv[0]);
//         return 1;
//     }

//     // 调用发送数据的函数
//     num_hosts = argc - 1;
//     send_data_to_hosts(num_hosts, argv + 1, data);

//     return 0;
// }
