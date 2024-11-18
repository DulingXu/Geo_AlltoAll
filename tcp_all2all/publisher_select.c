#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/select.h>

#define PORT 5555
#define BACKLOG 10
#define MAX_SUBSCRIBERS 10

typedef struct {
    int fd; 
    struct sockaddr_in address; 
} Subscriber;

int create_publisher(int* server_fd) {
    struct sockaddr_in address;

    if ((*server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Socket creation error");
        return -1;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(*server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        close(*server_fd);
        return -1;
    }

    if (listen(*server_fd, BACKLOG) < 0) {
        perror("Listen failed");
        close(*server_fd);
        return -1;
    }

    printf("Publisher started. Listening on port %d.\n", PORT);
    return 0;
}

int manage_connections(int server_fd, Subscriber* subscribers, int* num_subscribers) {
    fd_set read_fds;
    struct timeval tv;

    while (1) {
        FD_ZERO(&read_fds);
        FD_SET(server_fd, &read_fds);

        int max_fd = server_fd;

        for (int i = 0; i < *num_subscribers; i++) {
            if (subscribers[i].fd != -1) {
                FD_SET(subscribers[i].fd, &read_fds);
                if (subscribers[i].fd > max_fd) {
                    max_fd = subscribers[i].fd;
                }
            }
        }

        tv.tv_sec = 5; 
        tv.tv_usec = 0;

        int activity = select(max_fd + 1, &read_fds, NULL, NULL, &tv);
        if (activity < 0) {
            perror("Select error");
            return -1;
        }

        if (FD_ISSET(server_fd, &read_fds)) {
            int client_fd;
            socklen_t addr_len = sizeof(subscribers[*num_subscribers].address);
            if ((client_fd = accept(server_fd, (struct sockaddr*)&subscribers[*num_subscribers].address, &addr_len)) < 0) {
                perror("Accept failed");
                continue;
            }

            if (*num_subscribers < MAX_SUBSCRIBERS) {
                subscribers[*num_subscribers].fd = client_fd;
                (*num_subscribers)++;
                printf("Subscriber %d connected.\n", client_fd);
            } else {
                printf("Max subscribers reached. Closing connection.\n");
                close(client_fd); 
            }
        }

        for (int i = 0; i < *num_subscribers; i++) {
            if (subscribers[i].fd != -1 && FD_ISSET(subscribers[i].fd, &read_fds)) {
                char buffer[1024];
                int result = recv(subscribers[i].fd, buffer, sizeof(buffer), MSG_DONTWAIT);
                if (result <= 0) {
                    printf("Subscriber %d disconnected.\n", subscribers[i].fd);
                    close(subscribers[i].fd);
                    subscribers[i].fd = -1; 
                }
            }
        }
    }
}

void get_subscribers(Subscriber* subscribers, int num_subscribers) {
    printf("Current subscribers:\n");
    for (int i = 0; i < num_subscribers; i++) {
        if (subscribers[i].fd != -1) {
            printf("Subscriber %d: %s:%d\n", subscribers[i].fd,
                   inet_ntoa(subscribers[i].address.sin_addr),
                   ntohs(subscribers[i].address.sin_port));
        }
    }
}

void publish_message(Subscriber* subscribers, int num_subscribers, const char* message) {
    for (int i = 0; i < num_subscribers; i++) {
        if (subscribers[i].fd != -1) {
            send(subscribers[i].fd, message, strlen(message), 0);
        }
    }
}

//test
int main() {
    int server_fd;
    Subscriber subscribers[MAX_SUBSCRIBERS] = {0}; 
    int num_subscribers = 0;

    if (create_publisher(&server_fd) < 0) {
        return -1;
    }

    if (fork() == 0) {
        manage_connections(server_fd, subscribers, &num_subscribers);
        exit(0);
    }

    const char* message = "Hello, Subscribers!\n";
    while (1) {
        sleep(5);
        publish_message(subscribers, num_subscribers, message);
        get_subscribers(subscribers, num_subscribers);
    }

    close(server_fd);
    return 0;
}