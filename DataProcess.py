import json
from tweepy import Stream
from tweepy.streaming import StreamListener
import tweepy
from tweepy import OAuthHandler
 
consumer_key = 'vdLIrbn0VxPvb5lE5y8Ptk5zW'
consumer_secret = 'r9ygKXOf4GcmWJaPH0jQFESBezOGnkIRSa29BweIatuaKruLdp'
access_token = '445535548-lStLXyAVj11iyPYW7Ur0SASymRBOrLEZYWp2sZWk'
access_secret = '1ymELyIyt5T2Z2ayvQgbaq9aI0B4Tq0WFQmPAcxpj7DGQ'
 
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
 
api = tweepy.API(auth)

with open('python.json' ,'r') as f:
    line = f.readline()
    tweet = json.loads(line)
    print(json.dumps(tweet,indent=4))