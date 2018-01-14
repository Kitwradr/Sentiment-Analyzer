import tweepy
import simplejson as json

# Create variables for each key, secret, token
consumer_key = 'vdLIrbn0VxPvb5lE5y8Ptk5zW'
consumer_secret = 'r9ygKXOf4GcmWJaPH0jQFESBezOGnkIRSa29BweIatuaKruLdp'
access_token = '445535548-lStLXyAVj11iyPYW7Ur0SASymRBOrLEZYWp2sZWk'
access_token_secret = '1ymELyIyt5T2Z2ayvQgbaq9aI0B4Tq0WFQmPAcxpj7DGQ'

# Set up OAuth and integrate with API
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# Write a tweet to push to our Twitter account
#tweet = 'This tweet was tweeted using python script'
#api.update_status(status=tweet)
'''
for status in tweepy.Cursor(api.home_timeline).items(10):
    # Process a single status
    print(status.text)
'''

def process_or_store(tweet):
    print(json.dumps(tweet))
    
for friend in tweepy.Cursor(api.friends).items(): # list of all the followers
    process_or_store(friend._json)

