from User import User
import json


class Database:


    user_dict = {}

    def __init__(self,f_name):
        self.file_name = f_name

        f_p= open(f_name,"r")
        self.user_dict = json.load(f_p)
        f_p.close()


    def getTweets(self,cookie):
        
        # all_tweets ={}

        f_p = open(self.file_name,"r")

        data = json.load(f_p)
        f_p.close()

        return data
    

    def writeToDatabase(self,d):

        f_p = open(self.file_name,"w")
        json.dump(d,f_p,indent=6)
        f_p.close()


    def checkCookie(self,session):
        
        cookie = session.split("=")[0]
        return cookie in self.user_dict
    

    def verifyUser(self,session,u_name,p_word):
        
        resp = False
        if session in self.user_dict:
            
            resp = (self.user_dict[session]["Name"] == u_name and self.user_dict[session]["Password"]== p_word)

        return resp
    

    def addTweet(self,session,data):

        cookie = session.split("=")[0]

        user= self.user_dict[cookie]


        user["Tweets"].append(data)

        self.writeToDatabase(self.user_dict)


    def deleteTweet(self,session,id):

       user= self.user_dict[session]

       user["Tweets"].pop(int(id))
       self.writeToDatabase(self.user_dict)