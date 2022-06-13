// Server side C/C++ program to demonstrate Socket
// programming
#include <netinet/in.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <unistd.h>
#include<list>
#include<vector>
#include<iostream>
using namespace std;
#define PORT 8080
int main(int argc, char const* argv[])
{
    vector<int> wektor;
	while(true){
	
        int server_fd, new_socket, valread;
        struct sockaddr_in address;
        int opt = 1;
        int addrlen = sizeof(address);
        char buffer[1024] = { 0 };
        char* hello = "HTTP/1.1 200 OK\r\nServer: Apache/2.2.14 (Win32)\r\nContent-Length: 22\r\nContent-Type: text/html\r\n\r\n<h1>hello world!</h1>";
    
        // Creating socket file descriptor
        if ((server_fd = socket(AF_INET, SOCK_STREAM, 0)) == 0) {
            perror("socket failed");
            exit(EXIT_FAILURE);
        }
    
        // Forcefully attaching socket to the port 8080
        if (setsockopt(server_fd, SOL_SOCKET, SO_REUSEADDR | SO_REUSEPORT, &opt,sizeof(opt))) {
            perror("setsockopt");
            exit(EXIT_FAILURE);
        }
        address.sin_family = AF_INET;
        address.sin_addr.s_addr = INADDR_ANY;
        address.sin_port = htons(PORT);
    
        // Forcefully attaching socket to the port 8080
        if (bind(server_fd, (struct sockaddr*)&address,
                sizeof(address))< 0) {
            perror("bind failed");
            exit(EXIT_FAILURE);
        }
        if (listen(server_fd, 1000) < 0) {
            perror("listen");
            exit(EXIT_FAILURE);
        }
        if ((new_socket = accept(server_fd, (struct sockaddr*)&address,
                    (socklen_t*)&addrlen)) < 0) {
            perror("accept");
            exit(EXIT_FAILURE);
        }
        
        
        valread = read(new_socket, buffer, 1024); // zmienna odibiera char od wlochatego
        
        wektor.push_back(valread);
        cout << wektor.size() << " \n";
        printf("%s\n", buffer);
        send(new_socket, hello, strlen(hello), 0);
        printf("Madry Hello message sent\n");
    
    // closing the connected socket
        close(new_socket);
    // closing the listening socket
        shutdown(server_fd, SHUT_RDWR);
    }
    return 0;
}
