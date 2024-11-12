#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <ifaddrs.h>
#include <time.h>

#define PORT 3030
#define BUFFER_SIZE 1024
#define LOG_FILE "server_log.txt"

// 获取本地IP地址
void get_local_ip(char *ip_buffer) {
    struct ifaddrs *ifaddr, *ifa;
    void *tmp_addr_ptr = NULL;

    getifaddrs(&ifaddr); // 获取所有网络接口的地址信息
    for (ifa = ifaddr; ifa != NULL; ifa = ifa->ifa_next) {
        if (ifa->ifa_addr && ifa->ifa_addr->sa_family == AF_INET) { // IPv4地址
            tmp_addr_ptr = &((struct sockaddr_in *)ifa->ifa_addr)->sin_addr;
            inet_ntop(AF_INET, tmp_addr_ptr, ip_buffer, INET_ADDRSTRLEN);
            break; // 取得第一个有效IP后退出
        }
    }
    freeifaddrs(ifaddr); // 释放地址结构链表
}

// 记录客户端IP和接收时间到日志文件
void log_client_info(const char *client_ip) {
    FILE *log_file = fopen(LOG_FILE, "a");
    if (log_file == NULL) {
        perror("Failed to open log file");
        return;
    }

    // 获取当前时间
    time_t now = time(NULL);
    struct tm *time_info = localtime(&now);
    char time_str[20];
    strftime(time_str, sizeof(time_str), "%Y-%m-%d %H:%M:%S", time_info);

    // 写入日志文件
    fprintf(log_file, "Received from %s at %s\n", client_ip, time_str);
    fclose(log_file);
}

int main() {
    int server_fd, new_socket;
    struct sockaddr_in address;
    int addrlen = sizeof(address);
    char buffer[BUFFER_SIZE] = {0};
    char local_ip[INET_ADDRSTRLEN] = {0};
    char response[BUFFER_SIZE];

    // 获取本地IP地址
    get_local_ip(local_ip);

    // 创建服务器的套接字
    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    // 绑定端口和地址
    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr *)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    // 监听端口
    if (listen(server_fd, 3) < 0) {
        perror("Listen failed");
        close(server_fd);
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d\n", PORT);

    while (1) {
        printf("Waiting for a connection...\n");

        // 接受客户端的连接
        if ((new_socket = accept(server_fd, (struct sockaddr *)&address, (socklen_t*)&addrlen)) < 0) {
            perror("Accept failed");
            continue;
        }

        // 获取客户端的 IP 地址
        char client_ip[INET_ADDRSTRLEN];
        inet_ntop(AF_INET, &address.sin_addr, client_ip, INET_ADDRSTRLEN);
        printf("Connection from %s\n", client_ip);

        // 记录到日志文件
        log_client_info(client_ip);

        // 读取客户端发送的消息
        int valread = read(new_socket, buffer, BUFFER_SIZE - 1);
        if (valread > 0) {
            buffer[valread] = '\0'; // 确保字符串以 '\0' 结尾
            printf("Received: %s\n", buffer);

            // 创建带有本地IP地址的响应消息
            snprintf(response, sizeof(response), "ack from %s", local_ip);

            // 发送响应回客户端
            send(new_socket, response, strlen(response), 0);
            printf("Response sent: %s\n", response);
        } else {
            printf("No data received from client.\n");
        }

        // 关闭与客户端的连接
        close(new_socket);
    }

    close(server_fd);
    return 0;
}