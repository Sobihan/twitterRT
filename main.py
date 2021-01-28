from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener
import json
import os

try:
    API_KEY = os.environ['API_KEY']
    API_SECRET = os.environ['API_SECRET']
    ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
    ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
except:
    from setter import *

class twitter:
    def __init__(self):
        import tweepy
        self.auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
        self.auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(self.auth)
    def getAuth(self):
        return self.auth
    def getApi(self):
        return self.api
    def postTweet(self, message):
        self.api.update_status(message)
    def retweet(self, idTweet):
        try:
            self.api.retweet(idTweet)
            print("Rt success")
            return True
        except:
            print("RT ERROR")
            return False
    def like(self, idTweet):
        try:
            self.api.create_favorite(idTweet)
            print("Like Sucess")
        except:
            print("Like not sucess")

TW = twitter()

class TweetListener(StreamListener):
    def on_data(self, data):
        jsonData = json.loads(data)
        print("=================")
        if(TW.retweet(jsonData['id'])):
            print(jsonData["text"])
        if  TW.like(jsonData['id']):
            print(jsonData["text"])
        print("=================")
        return True
    def on_error(self, status):
        print (status)


def parseTrigger(path = "file.json"):
    try:
        f = open(path)
    except:
        print("Need ", file, sep='')
        exit(84)
    data = json.load(f)
    hashtags = data['hashtag']
    trueHashtags = []
    for h in hashtags:
        if data['hashtag'][h]:
           trueHashtags.append(h)
    return trueHashtags

banWords = parseTrigger()
listener = TweetListener()
auth = TW.getAuth()
stream = Stream(auth, listener)
stream.filter(track=hashtags)
