import socket
import threading
import json
from requestHandler import RequestHandler
import sys

HOST = '127.0.0.1'
PORT = 8165

SOMETHING_BROKEN='''HTTP/1.1 502 Bad Gateway\r\nContent-Type: text/html\r\n\r\n<html><head></head><body><h1>OOps something bad happended</h1></body></html>
                    '''
handler = RequestHandler()

def thread_func(connection, address):


    with connection:
                
        try:
            data = connection.recv(1024)
            
            if data:
                data = data.decode("UTF-8")

        
                data_tuple= (data,address)
                
                response= handler.parseRequest(data_tuple)
                
                if(response):                       

                    connection.send(response.encode("UTF-8"))
                else:
                    connection.send(SOMETHING_BROKEN.encode("UTF-8"))

        except Exception as e:
            
            connection.send(SOMETHING_BROKEN.encode("UTF-8"))
            connection.close()
            sys.exit(0)





with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as listening_socket:

    listening_socket.bind((HOST,PORT))
    listening_socket.listen()
    
    while True:

        try:
            connection, address = listening_socket.accept()
            
            new_thread = threading.Thread(target=thread_func,args=(connection, address))
            new_thread.start()
            

        except KeyboardInterrupt as e:
            break
            
        except Exception as e:
            connection.send(SOMETHING_BROKEN.encode("UTF-8"))
            listening_socket.close()
            sys.exit(0)


    print("Exiting")