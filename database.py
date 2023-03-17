import json
from User import User
class Database:

    user_dict = {}
    
    def __init__(self,f_name):
        self.file_name= f_name

        f_p= open(f_name,"r")

        self.user_dict = json.load(f_p)



        
        
    def getTweets(self):
        
        all_tweets = []
        # response = ''
        
        file_pointer= open(self.file_name,"r")

        json_dict = json.load(file_pointer)

        

        for each_entry in json_dict:
            all_tweets.append(json_dict[each_entry]["Tweets"]) 


        # for each_list in all_tweets:
        #     for each_t in each_list:
        #         response += each_t + '\n'

        file_pointer.close()
        return (all_tweets)
    

    def writeToDatabase(self,d):

        f_pointer = open(self.file_name,"w")
        json.dump(d,f_pointer,indent=6)

        f_pointer.close()


    def addUser(self,session_id,username,password):
        user = User(username,password) 

        self.user_dict[username]= user.getUserInfo()
        self.writeToDatabase(self.user_dict)

    def checkCookie(self,uname):

        return (self.user_dict["uname"]["Name"] == uname)



    def checkUser(self,u_name,p_word):

        resp = False

        for each_user in self.user_dict:
            
            if(self.user_dict[each_user]["Name"] == u_name and self.user_dict[each_user]["Password"] == p_word):
                   
                return True
        
        
        return resp


    # def verifyUser(self,session,u_name):
        
    #     if( session in self.user_dict):
    #         user= self.user_dict[session]
    #         if(user["Name"] == u_name):
    #             return True
    #         else:
    #             return False

    #     else:
    #         return False
        

    def addTweet(self,session,data):
    
        user= self.user_dict[str(session)]
        
        user["Tweets"].append(data)
        # self.user_dict[str(session)]= user.getUserInfo()
        self.writeToDatabase(self.user_dict)