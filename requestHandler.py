import json
import os
from database import Database


OK_HDR = "HTTP/1.1 200 OK\r\n"

UN_HDR = "HTTP/1.1 401 Unauthorized\r\nContent-Type: text/html\r\n"
UN_BDY = "<html><head></head><body><h1>401 Unauthorized</h1></body></html>"


BR_HDR = "HTTP/1.1 400 Bad Request\r\nContent-Type: text/html\r\n"
BR_BDY = "<html><head></head><body><h1>400 Bad Request</h1></body></html>"

NF_HDR = "HTTP/1.1 404 NOT FOUND\r\nContent-Type: text/html\r\n"
NF_BD = "<html><head></head><body><h1>404 File not found</h1></body></html>"

class RequestHandler:

    def __init__(self):
        self.d_base = Database("database.json")


    def parseRequest(self,data_o):
        
        header_dict = {}

        request = data_o[0]
        user_ip = data_o[1]

        response=""
        
        if(len(request.split('\r\n\r\n')) >= 2):

            

            header = request.split('\r\n\r\n')[0]
            body = request.split('\r\n\r\n')[1]

            lines = header.split('\r\n')

            first_line = lines.pop(0)
            

            verb = first_line.split(" ")[0] 
            path = first_line.split(" ")[1]

            
            for each_line in lines:
                
                if len(each_line.split(": ")) != 2:
                    
                    response = BR_HDR+'\r\n'+BR_BDY
                else:
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
                    response = BR_HDR+'\r\n'+BR_BDY

        else:
            
            response = BR_HDR+'\r\n'+BR_BDY
        
        return response
    

    def loadIndex(self):

        f_p = open("index.html")

        body = f_p.read()

        f_p.close()
        return OK_HDR+"\r\n"+body
    


    def apiRequest(self,verb,path,h_dict,content):

        return_data=""
        
        
        if (verb == "GET" and path == '/api/tweet'):
            
            

            if('Cookie' in h_dict):
                body = json.dumps(self.d_base.getTweets(h_dict['Cookie'].split("=")[0]))
                header= OK_HDR+"Content-Type: application/json\r\n"
                
                return_data = (header+"\r\n"+body)
            else:
                return_data = UN_HDR + "\r\n"+ UN_BDY

        elif verb == 'POST':

            return_data = self.managePost(path,h_dict,content)

        elif (verb == 'DELETE' and path.split('/')[1]=='api' and path.split('/')[2]=='tweet'):

            t_id= path.split('/')[3]

            if(int(t_id) >= 0):
                
                if('Cookie' in h_dict):
    
                    user_cookie= h_dict['Cookie']

                    if(self.d_base.checkCookie(user_cookie)):

                        self.d_base.deleteTweet(h_dict['Cookie'].split("=")[0],t_id)
                        return_data = OK_HDR+"\r\n"

                    else:
                        return_data = UN_HDR + "\r\n"+ UN_BDY
               
                else:
                    return_data = UN_HDR + "\r\n"+ UN_BDY

            else:
                return_data = BR_HDR + "\r\n"+ BR_BDY   


        elif (verb == 'DELETE' and path.split('/')[1]=='api' and path.split('/')[2]=='login'):
            
            

            if('Cookie' in h_dict):

                user_cookie= h_dict['Cookie']

                if(self.d_base.checkCookie(user_cookie)):


                    username = h_dict["Cookie"].split("=")[1]
                    header = OK_HDR+"Content-Type: text/html\r\n"

                    body= '''
                            <input type="text" id="Name" value="Username"><br><br>
                            <input type="text" id="Password" value="Password"><br><br>
                            <button onclick="logIn()">Log In</button>'''


                    cookie = "Set-Cookie: " + '0x00000249C1030EA0'+"="+username+";Expires=Thu, May 19 2000 00:00:00 UTC;Path=/"+'\r\n'
                    header += cookie

                    return_data = header + '\r\n'+body

                else:
                    return_data = UN_HDR + "\r\n"+ UN_BDY

            else:
                return_data = UN_HDR + "\r\n"+ UN_BDY

        
        else:
            return_data = BR_HDR + "\r\n" +BR_BDY 

        return (return_data)
    
    def managePost(self,path,h_dict,content):

        
        return_data=""

        if(path == '/api/login'):
            
            

            username_k_v = content.split('&')[0]
            password_k_v = content.split('&')[1]


            username = username_k_v.split('=')[1]
            password = password_k_v.split('=')[1]



            # In a regular case there would be a function here
            # that find a user verify it and then set the cookie here based
            # on thr session id in the user.

            if self.d_base.verifyUser('0x00000249C1030EA0',username,password):
                

                header = OK_HDR+"Content-Type: text/html\r\n"

                body='''
                        <div id="login">
                        <input type="text" id="Tweet" value="Enter your Thoughts"><br><br>
                        <button onclick="Tweet()">Tweet</button>
                        <br>
                        <br>
                        <button onclick="Logout()">Log Out</button>
                        <br>
                        <br>
                        <h2>Tweets</h2>
                        </div>'''
                        
                cookie = "Set-Cookie: " + '0x00000249C1030EA0'+"="+username+";Path=/"+'\r\n'
                header += cookie

                
                return_data = header + '\r\n'+body

            else:
                return_data= UN_HDR + "\r\n" + UN_BDY

        elif( path == '/api/tweet'):
            
            if 'Cookie' in h_dict:

                user_cookie= h_dict['Cookie']
                
                if(self.d_base.checkCookie(user_cookie)):
                    self.d_base.addTweet(user_cookie,(content))
                    
                    return_data = OK_HDR+"\r\n"
                else:
                    return_data = UN_HDR+'\r\n'+UN_BDY
                

            else:
                return_data = UN_HDR+'\r\n'+UN_BDY
        else:
            return_data = BR_HDR + '\r\n' +BR_BDY

        return return_data
    

    def fileRequest(self,rel_path):

        return_data=""

        try:
            absolute_path = os.path.dirname(__file__)
            l=(rel_path.split('/'))


            

            l.pop(0)

            extension= rel_path.split(".")[1]

            relative_path="/".join(l)

            full_path=os.path.join(absolute_path, relative_path)

            if(extension == 'html' ):
                f_p = open(full_path)
                header = OK_HDR
                body = f_p.read()
                f_p.close()
            else:
                f_p = open(full_path,'rb')
                body = f_p.read()

                header = OK_HDR+"Content-Type: image/webp\r\n"
                body.encode('UTF-8')
                header +="Content-Lenght: "+os.path.getsize(full_path) + "\r\n"
                f_p.close()

            return_data= header+"\r\n" + body



        except:
            return_data = NF_HDR +'\r\n'+ NF_BD

        return return_data

