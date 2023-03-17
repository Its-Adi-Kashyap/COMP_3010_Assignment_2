// started with https://www.educative.io/edpresso/how-to-implement-tcp-sockets-in-c
// and the example in https://www.man7.org/linux/man-pages/man3/getaddrinfo.3.html

#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <assert.h>
#include <netdb.h> // For getaddrinfo
#include <unistd.h> // for close
#include <stdlib.h> // for exit
int main(int argc, char *argv[])
{

    if (argc != 3 ){
        printf("Please provide [filename][cookie][memo]");
        return -1;
    }
    else{
       char* session = argv[1];
       char*  memo = argv[2];
    

        int socket_desc;
        struct sockaddr_in server_addr;
        char server_message[2000], client_message[2000];
        char address[100];

        struct addrinfo *result;
        
        // Clean buffers:
        memset(server_message,'\0',sizeof(server_message));
        memset(client_message,'\0',sizeof(client_message));
        
        // Create socket:
        socket_desc = socket(AF_INET, SOCK_STREAM, 0);
        
        if(socket_desc < 0){
            printf("Unable to create socket\n");
            return -1;
        }
        
        printf("Socket created successfully\n");

        struct addrinfo hints;
        memset (&hints, 0, sizeof (hints));
        hints.ai_family = PF_UNSPEC;
        hints.ai_socktype = SOCK_STREAM;
        hints.ai_flags |= AI_CANONNAME;
        
        // get the ip of the page we want to scrape
        int out = getaddrinfo ("130.179.28.113", NULL, &hints, &result);
        // fail gracefully
        if (out != 0) {
            fprintf(stderr, "getaddrinfo: %s\n", gai_strerror(out));
            exit(EXIT_FAILURE);
        }
        
        // ai_addr is a struct sockaddr
        // so, we can just use that sin_addr
        struct sockaddr_in *serverDetails =  (struct sockaddr_in *)result->ai_addr;
        
        // Set port and IP the same as server-side:
        server_addr.sin_family = AF_INET;
        server_addr.sin_port = htons(8165);
        //server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
        server_addr.sin_addr = serverDetails->sin_addr;
        
        // converts to octets
        printf("Convert...\n");
        inet_ntop (server_addr.sin_family, &server_addr.sin_addr, address, 100);
        printf("Connecting to %s\n", address);
        // Send connection request to server:
        if(connect(socket_desc, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0){
            printf("Unable to connect\n");
            exit(EXIT_FAILURE);
        }
        printf("Connected with server successfully\n");
        

        //MAKING A POST
// =======================================================================================================
        char* post_header="";

        asprintf(&post_header, "POST /api/tweet HTTP/1.1\r\nCookie: %s\r\n\r\n%s",session,memo);

        char post_request[] = "";
        
        strncat(post_request,post_header,strlen(post_header));

        printf("Sending:\n%s\n", post_request);
        // Send the message to server:
        printf("Sending request, %lu bytes\n", strlen(post_request));
        if(send(socket_desc, post_request, strlen(post_request), 0) < 0){
            printf("Unable to send message\n");
            return -1;
        }
        
        // Receive the server's response:
        if(recv(socket_desc, server_message, sizeof(server_message), 0) < 0){
            printf("Error while receiving server's msg\n");
            return -1;
        }
        
        printf("Server's response: %s\n",server_message);
        

     // Close the socket:
        close(socket_desc);

// =================================================================================================
        //MAKING A GET 


        socket_desc = socket(AF_INET, SOCK_STREAM, 0);
        
        if(socket_desc < 0){
            printf("Unable to create socket\n");
            return -1;
        }
        
        printf("Socket created successfully\n");
        
        // converts to octets
        printf("Convert...\n");
        inet_ntop (server_addr.sin_family, &server_addr.sin_addr, address, 100);
        printf("Connecting to %s\n", address);
        // Send connection request to server:
        if(connect(socket_desc, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0){
            printf("Unable to connect\n");
            exit(EXIT_FAILURE);
        }
        printf("Connected with server successfully\n");


        char* get_header="";

        asprintf(&get_header, "GET /api/tweet HTTP/1.1\r\nCookie: %s\r\n\r\n",session);
        char get_request[] = "";
        
        strncat(get_request,get_header,strlen(get_header));
        printf("%s",get_request);
        printf("Sending:\n%s\n", get_request);
        // Send the message to server:
        printf("Sending request, %lu bytes\n", strlen(get_request));
        
        if(send(socket_desc, get_request, strlen(get_request), 0) < 0){
            printf("Unable to send message\n");
            return -1;
        }
        
        // Receive the server's response:
        if(recv(socket_desc, client_message, sizeof(client_message), 0) < 0){
            printf("Error while receiving server's msg\n");
            return -1;
        }
        

        char* ret= strstr(client_message,memo);
        
        ret[strlen(memo)+1]='\0';

// ===========ASSERT======================================
        assert(strcmp(ret,memo));

        close(socket_desc);




// DELETING

// =====================================================================


        socket_desc = socket(AF_INET, SOCK_STREAM, 0);
        
        if(socket_desc < 0){
            printf("Unable to create socket\n");
            return -1;
        }
        
        printf("Socket created successfully\n");
        
        // converts to octets
        printf("Convert...\n");
        inet_ntop (server_addr.sin_family, &server_addr.sin_addr, address, 100);
        printf("Connecting to %s\n", address);
        // Send connection request to server:
        if(connect(socket_desc, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0){
            printf("Unable to connect\n");
            exit(EXIT_FAILURE);
        }
        printf("Connected with server successfully\n");

        char* bad_guy= "0x000001C8FC9DBD80";
        char* del_header="";

        asprintf(&del_header, "DELETE /api/tweet/0 HTTP/1.1\r\nCookie: %s\r\n\r\n",bad_guy);
        char del_request[] = "";
        
        strncat(del_request,del_header,strlen(del_header));
        printf("%s",del_request);
        printf("Sending:\n%s\n", del_request);
        // Send the message to server:
        printf("Sending request, %lu bytes\n", strlen(del_request));
        
        if(send(socket_desc, del_request, strlen(del_request), 0) < 0){
            printf("Unable to send message\n");
            return -1;
        }
        
        // Receive the server's response:
        if(recv(socket_desc, client_message, sizeof(client_message), 0) < 0){
            printf("Error while receiving server's msg\n");
            return -1;
        }
        

        close(socket_desc);


    }
    return 0;
}
