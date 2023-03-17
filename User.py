import json
class User:

    # def __init__(self,n,p):
    #     self.tweets=[]
    #     self.name= n
    #     self.password= p


    # def addTweet(self,t):
    #     self.tweets.append(t)

    # def getAllTweets(self):
    #     return self.tweets

    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__, 
    #         sort_keys=True, indent=4)

    def __init__(self,n,p):
        self.user = {}
        self.user["Name"] = n
        self.user['Password'] = p
        self.user['Tweets'] =[]
    
    def getUserInfo(self):
        return self.user