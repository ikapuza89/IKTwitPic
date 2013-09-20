import sys
import tweepy
import time
import threading
import os

consumer_key="X"
consumer_secret="X"
access_key = "X"
access_secret = "X" 

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)

class Timer(threading.Thread):
    def __init__(self, seconds):
        self.runTime = seconds
        threading.Thread.__init__(self)
    def run(self):
        time.sleep(self.runTime)

class CountDownTimer(Timer):
    def run(self):
        counter = self.runTime
        for sec in range(self.runTime):
            print counter
            time.sleep(1.0)
            counter -= 1

class CountDownExec(CountDownTimer):
    def __init__(self, seconds, action):
        self.action = action
        CountDownTimer.__init__(self, seconds)
    def run(self):
        CountDownTimer.run(self)
        self.action()
		
def takePicture():
    os.system('raspistill -o picture.jpg -t 0')
    
c = CountDownExec(5, takePicture)
        
class CustomStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        print status.user.id
        print status.user.screen_name
        print status.id
        print status.text
        c.start()

    def on_error(self, status_code):
        print >> sys.stderr, 'Encountered error with status code:', status_code
        return True # Don't kill the stream

    def on_timeout(self):
        print >> sys.stderr, 'Timeout...'
        return True # Don't kill the stream

sapi = tweepy.streaming.Stream(auth, CustomStreamListener())
sapi.filter(track=['#hashtag @username'])
