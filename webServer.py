import socket
import threading
import json
from requestHandler import RequestHandler
import sys

HOST = '127.0.0.1'
PORT = 8165


handler = RequestHandler()



with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as listening_socket:
    
    listening_socket.bind((HOST,PORT))
    listening_socket.listen()

    
    while True:

        try:

            connection, address = listening_socket.accept()

            with connection:
                
                data = connection.recv(1024)
                
                if data:
                    data = data.decode('UTF-8')

                    data_tuple= (data,address)
                    
                    # request= json.dumps(data_tuple)
                    
                    response= handler.parseRequest(data_tuple)

                    connection.send(response.encode('utf-8'))
                        
        except KeyboardInterrupt as e:
            listening_socket.close()
            sys.exit(0)

        except Exception as e:
            sys.exit(0)