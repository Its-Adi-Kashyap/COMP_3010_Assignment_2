import json
class User:

    def __init__(self,n,p,s):
        self.user = {}
        self.user["Name"] = n
        self.user['Password'] = p
        self.user['Session'] = s
        self.user['Tweets'] =[]
    
    def getUserInfo(self):
        return self.user