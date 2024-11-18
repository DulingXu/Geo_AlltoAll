#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>
#include <pthread.h>

#define PORT 8080
#define MAX_SUBSCRIBERS 10
#define BUFFER_SIZE 256

typedef struct {
    int socket;
} Subscriber;

Subscriber *subscribers[MAX_SUBSCRIBERS];
int subscriber_count = 0;
pthread_mutex_t lock;

void create_publisher() {
    int server_socket;
    struct sockaddr_in server_address;

    server_socket = socket(AF_INET, SOCK_STREAM, 0);
    if (server_socket < 0) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(PORT);

    if (bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0) {
        perror("Bind failed");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    if (listen(server_socket, MAX_SUBSCRIBERS) < 0) {
        perror("Listen failed");
        close(server_socket);
        exit(EXIT_FAILURE);
    }

    printf("Publisher created, waiting for subscribers...\n");

    while (1) {
        Subscriber *sub = malloc(sizeof(Subscriber));
        socklen_t addr_len = sizeof(sub->socket);
        sub->socket = accept(server_socket, NULL, &addr_len);
        if (sub->socket < 0) {
            perror("Accept failed");
            free(sub);
            continue;
        }

        pthread_mutex_lock(&lock);
        if (subscriber_count < MAX_SUBSCRIBERS) {
            subscribers[subscriber_count++] = sub;
            printf("New subscriber connected.\n");
        } else {
            printf("Max subscribers reached. Rejecting new connection.\n");
            close(sub->socket);
            free(sub);
        }
        pthread_mutex_unlock(&lock);
    }

    close(server_socket);
}

void publish(const char *message) {
    pthread_mutex_lock(&lock);
    for (int i = 0; i < subscriber_count; ++i) {
        send(subscribers[i]->socket, message, strlen(message), 0);
    }
    pthread_mutex_unlock(&lock);
}

int main() {
    pthread_mutex_init(&lock, NULL);

    pthread_t publisher_thread;
    if (pthread_create(&publisher_thread, NULL, create_publisher, NULL) != 0) {
        perror("Failed to create publisher thread");
        return -1;
    }
    const char* message = "Hello, Subscribers!\n"; 
    publish(message);
    pthread_join(publisher_thread, NULL);

    pthread_mutex_destroy(&lock);
    return 0;
}
