#extending functionality of existing program:
#sets the DM check as a threaded task occuring every 15 minutes
#while allowing the temperature/humidty readouts to occur more regularly

#also reads/writes DM_ID from a file so that when a new session boots up
#the ID from the last time the program ran is available and won't interfere
#with the new sessions functionality

#######stuff to do##############
# need to add a class for humiditry reading to update screen and twitter account
#need to add error codes/exception handling for: twitter refusing access, internet being down

import queue
import threading
import random
import tweepy
import time
from auth import (
    consumer_key,
    consumer_secret,
    access_token,
    access_token_secret
)

authDM = tweepy.OAuthHandler(consumer_key, consumer_secret)
authDM.set_access_token(access_token, access_token_secret)


def updateScreen(num):
    while True:
        #need code to read humidity and print it on the screen here.
        print("The current number is " + str(num))
        num = num +1

def updateTwitter(authDM, num):
    api = tweepy.API(authDM)
    api.update_status("the number is " + str(num*random.randrange(2,100)))


def DMCheck(authDM, num):
    textCheck = None
    while True:
        api = tweepy.API(authDM)
        file = open("DM_ID.txt","r")
        idCheck = file.read()        
        file.close()
        
        
        message = api.list_direct_messages()
        recentMessage = message[0]


        #checks the most recent stored message ID, if different then checks for 'turn off' and returns True
        if recentMessage.id != idCheck:
            idCheck = recentMessage.id
            textCheck = recentMessage.message_create["message_data"]["text"]
            print("The current DM is "+textCheck)
            file  = open("DM_ID.txt","w")
            file.write(idCheck)
            file.close()
            if textCheck == "turn off":
                return True
            #updates the twitter account  - need to swap num for Humidty details
        updateTwitter(authDM, num)
        time.sleep(60*15)
    
#represents the humid/temp values that will be passed around the program
num = 1

#create queue to store return value from thread function
que = queue.Queue()

#set thread function and queue to store return via lambda function
t = threading.Thread(target = lambda q, arg1, arg2: q.put(DMCheck(arg1, arg2)), args =[que,authDM, num], daemon = True) # the arguments on this line (and elsewhere most likely) need amending to sort this code out!

#initialise thread
t.start()



#main routine

flag = False
while flag == False:
    
    #this would be the line where a function is called to output details to a screen. Can remove the time sleep element
    print("looped")
    try:
        #where the return value from the thread funtion is processed. If return is true programme ends
        
        flag = que.get(False)
               
           
    except queue.Empty:
        print("the queue is empty")
    time.sleep(60*2)
        
    
   
print("the system has turned off")
    
    
