# COMP_3010_Assignment_2

## An API Web Serve. with system tests and complete tests. 
>A Web API server that lets you make and delete tweets,it also lets you see what others are talking about (A really horizontal version). Also, it lets you fetch files from the server.

### AUTHOR: Aditya Kashyap,7895430

- This code was written on windows and tested on both windows and Aviary with Google Chrome.
- Total package contains 9 files including the fake database.(excluding the Files-distributed folder)

### HOW IT RUN:

1. Start the server first. 
    >To run the server simply put in the command `python3 webServer.py` in the terminal.  
2. After the server is running Connect to it using any desired agent.

    > By default the _Ip_ for the server is `127.0.0.1` and the port number is `8165`.These can be changed any time from line 7 and 8 in webServer.py

3. **For logging-in the Name that is set by default is _`Muhamad`_ and password is _`Lama`_. and the session id is: 0x00000249C1030EA0**. 

4. To run the **scrapper** type the simply run type `make` or the following command in the terminal:
    > `clang scrapper.c -o scrapper `  

5. And then simply run the executable `scrapper`


### UNDER THE HOOD:

- There are a lot of moving parts in the whole project.
- `database.json` is the _fake Database_ that cointains the user data.
    > User data is just a json Object with fields such as name,password,sessionid, and tweets.
    > each user is stored in key value pairs with the cookie set as the key.
- `database.py` is the data layer that just takes care of handeling the data such as   adding tweet,deleting tweet, verifying user etc.
- `requestHandler.py` is the main logic layer that takes care of all the data movement and logic. All the requests after comming in are  handed down to the _requestHandler_ which then parses,and takes appropriate action based on the request.  
- In the end it returns the response(cointaing all the headers set and content in the body where applicable) that is sent back on the socket.  
- `webHandler's.py` only job is to make a TCP connection using sockets and then use multithreading.  
- `scrapper` is more or less like a test file that has a few assersts to check if the server is working correctly.
- All of the front end stuff is inside `index.html` thats where the XMLHTTP requests are made and the content of the pages are changed accordingly.  
- `User` is just a future addition to the project where we can add new users.

### OVER THE HOOD?:
- As soon as the **GET** request is made to the server by the web Browser, it launches index.html with the log-in page kicking off the entire game.  
- Then if the correct user name and password are entered then it shows you the tweets that you made and what the other people made.
- You can also delete your tweets by pressing the delete button. 
    >However you can only delete your own tweets. 
- If you want to fetch a file simply add the path in the url.  


## NOTES:

* On Windows the server does not instantly shuts down when interupted by _ctrl + c_ it shuts down after another call to the it has been made(it refuses the call and then shuts down).
* The web Server works with persistance and has full functionality including setting and deleting cookies.
* The file fetching works, its just without the images.
* On line 196 and 213 I hard coded the session id to set and verify because we just need to set up one working account.
* The scrapper just POST's and GET's the tweet and asserts (which passes) but it just does one DELETE without actually checking anythig.


### SUB-NOTE:

###### This was the first time i ever worked on any kind of front end development, which would be quite obvious from the monstrosity of the 'index.html' and all the script and functions in it. Please ignore the mess in there as i was learning it and doing it together.All in all I really had fun doing the assignment.
Thanks.