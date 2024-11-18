#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <sys/select.h>
#include <pthread.h>

#define PORT 5555
#define BACKLOG 10
#define MAX_SUBSCRIBERS 10

typedef struct {
    int fd; 
    struct sockaddr_in address; 
} Subscriber;

Subscriber subscribers[MAX_SUBSCRIBERS] = {0}; 
int num_subscribers = 0; 
int server_fd; 

void* create_publisher(void* arg) {
    struct sockaddr_in address;

    if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("Socket creation error");
        return NULL;
    }

    address.sin_family = AF_INET;
    address.sin_addr.s_addr = INADDR_ANY;
    address.sin_port = htons(PORT);

    if (bind(server_fd, (struct sockaddr*)&address, sizeof(address)) < 0) {
        perror("Bind failed");
        close(server_fd);
        return NULL;
    }

    if (listen(server_fd, BACKLOG) < 0) {
        perror("Listen failed");
        close(server_fd);
        return NULL;
    }

    printf("Publisher started. Listening on port %d.\n", PORT);

    while (1) {
        int client_fd;
        socklen_t addr_len = sizeof(subscribers[num_subscribers].address);
        if ((client_fd = accept(server_fd, (struct sockaddr*)&subscribers[num_subscribers].address, &addr_len)) < 0) {
            perror("Accept failed");
            continue;
        }

        if (num_subscribers < MAX_SUBSCRIBERS) {
            subscribers[num_subscribers].fd = client_fd;
            num_subscribers++;
            printf("Subscriber %d connected.\n", client_fd);
        } else {
            printf("Max subscribers reached. Closing connection.\n");
            close(client_fd); 
        }
    }

    return NULL; 
}

int get_info(char* addresses[], int* ports[]) {
    int count = 0;

    for (int i = 0; i < num_subscribers; i++) {
        if (subscribers[i].fd != -1) {
            addresses[count] = inet_ntoa(subscribers[i].address.sin_addr);
            ports[count] = ntohs(subscribers[i].address.sin_port);
            count++;
        }
    }

    return count;
}

void publish_message(const char* message) {
    for (int i = 0; i < num_subscribers; i++) {
        if (subscribers[i].fd != -1) {
            send(subscribers[i].fd, message, strlen(message), 0);
        }
    }
}

int main() {
    pthread_t publisher_thread;

    if (pthread_create(&publisher_thread, NULL, create_publisher, NULL) != 0) {
        perror("Failed to create publisher thread");
        return -1;
    }

    const char* message = "Hello, Subscribers!\n";
    while (1) {
        sleep(5); 
        publish_message(message);

        char* addresses[MAX_SUBSCRIBERS];
        int ports[MAX_SUBSCRIBERS];
        int count = get_info(addresses, ports);

        printf("Currently connected subscribers (%d):\n", count);
        for (int i = 0; i < count; i++) {
            printf("Subscriber %d: %s:%d\n", i + 1, addresses[i], ports[i]);
        }
    }

    close(server_fd);
    pthread_join(publisher_thread, NULL);
    return 0;
}