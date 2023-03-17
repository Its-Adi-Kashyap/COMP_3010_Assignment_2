# Check cookies and see if they exist or not
# if not then set the cookie but do not let to do any API stuff
#  
#
import json
import uuid
import sys
from database import Database


class RequestHandler:

    def __init__(self):
        self.d_base = Database("database.json")


    def parseRequest(self,data_o):


        header_dict = {}
        
        response=''

        request = data_o[0]
        user_ip = data_o[1]

        header = request.split('\r\n\r\n')[0]
        body = request.split('\r\n\r\n')[1]
        
        lines = header.split('\r\n')

        first_line = lines.pop(0)
        

        verb = first_line.split(" ")[0] 
        path = first_line.split(" ")[1]


        for each_line in lines:
            key = each_line.split(': ')[0]
            value = each_line.split(': ')[1]
            header_dict[key] = value

        if not path.split('/')[1].strip():
            response = self.loadIndex()

        else:
            if(path.split('/')[1] == 'api'):
                response= self.apiRequest(verb,path,header_dict,body)
            elif(verb == 'GET' and path.split('/')[1] != 'api'):
                response= self.fileRequest(path)
            else:
                response = "HTTP/1.1 400 BAD REQUEST\r\n\r\n<html><head><h1>BAD REQUEST</h1></head></html>"
        
        return response



    def loadIndex(self):

        file_pointer= open("index.html")

        header = "HTTP/1.1 200 OK\r\n\Content-Type: text/html\n\r\n\r"
        body= file_pointer.read()
        file_pointer.close()
        return header+body



    def checkCookie(self,u_cookie):
        
        
        # s_id = u_cookie.split("=")[0]
        u_name = u_cookie.split("=")[1]

        return (self.d_base.checkCookie(u_name))


    def managePost(self,path,h_dict,content):
        response = ""
        
        return_header = ''
        return_body = ''


        if( path == '/api/tweet'):
            
            if 'Cookie' in h_dict:
                
                user_cookie= h_dict["Cookie"]
                data_type = h_dict['Content-Type'] 

                if data_type == 'application/json':
                #Content is json
                    if(self.checkCookie(user_cookie)):

                        print("here")

                        self.d_base.addTweet(user_cookie,content)
                        return_header= "HTTP/1.1 200 OK \r\n\r\n"
                        return_body = self.d_base.getTweets()
                        response = return_header + json.dumps(return_body)

                    else:
                        response= "HTTP/1.1 401 UNAUTHORISED\r\n\r\n"

            else:
                response = "HTTP/1.1 401 UNAUTHORISED\r\n\r\n"


        elif path == '/api/login':

            
            username_k_v = content.split('&')[0]
            password_k_v = content.split('&')[1]


            username = username_k_v.split('=')[1]
            password = password_k_v.split('=')[1]

            session_id = username


            if self.d_base.checkUser(username,password):

                return_header = 'HTTP/1.1 200 OK\r\nContent-Type: application/json; charset=utf-8\r\n'

                ptr = open("logedIn.html")
                return_body= ptr.read()
                
                ptr.close()
                length = len(return_body)

                return_header += "Content-Length: {}\r\n".format(length)

                cookie = "Set-Cookie: " + str(session_id)+"="+str(username) +"\r\n"
                return_header += cookie

                response = return_header+'\r\n'+ (return_body)
            else:
                response =("HTTP/1.1 404 UNATUTHORISED\r\nContent-Type: text/html\r\n\r\n<html><head><h1>Not A User</h1></head></html>")

        else:
            response = "HTTP/1.1 400 BAD REQUEST\r\n\r\n"

        return response



    def apiRequest(self,verb,pth,h_dict,content):
        
        response = ''

        
        if (verb == 'GET' and pth == '/api/tweet'):
           
           if 'Cookie' in h_dict:
                response_body= self.d_base.getTweets()

                response ="HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
                response += json.dumps(response_body)
           else:
               response= "HTTP/1.1 401 UNAUTHERISED\r\n\r\n<html><head><h1>Not Logged In</h1></head></html>" 
        elif verb == 'POST':
            response = self.managePost(pth,h_dict,content)

        elif verb == 'DELETE':
            pass
        else:
            response = "HTTP/1.1 400 BAD REQUEST\r\n\r\n<html><head><h1>BAD REQUEST</h1></head></html>"
        
        return response
        



    def fileRequest(self,pth):

        response_header=''
        respones_body = ''






        try:
            f_p = open(pth)

            response_header = "HTTP/1.1 200 OK\r\n\Content-Type: text/html\r\n\r\n"
            respones_body= f_p.read()

        except:
            response_header="HTTP/1.1 404 NOT FOUND"
            response_body = "<html><head><h1> File Not found. Please check the path.</h1></head></html>"

        
        return response_header+respones_body