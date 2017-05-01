#!/usr/bin/env python
# KEYWORDS STREAMER
# The streamer is listening to a list of keywords, defined at the beginning. Using tweepy module to authenticate with Twitter and stream the tweets;

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from auth import TwitterAuthKeywords

"""
----------------
K E Y W O R D S
----------------
"""
# list of keywords to listen to; should include these when appear as hashtag too (e.g. architecture, #architecture)
keywords = ['BIM', 'DynamoBIM', 'Revit', 'AutoCAD', 'Autodesk', 'Rhinoceros 3D', 'Grasshopper 3D', 'Rhino 3D', 'CAAD', 'computer-aided', 'data-driven', 'model-based', '3dprint', 'parametric', 'parametricism',  'parametricist']

"""
----------------
S T R E A M E R
----------------
"""
#This is a basic listener that updates the keywords_tweets.json file every time it received tweets
class StdOutListener(StreamListener):

    def on_data(self, data):
        #print data
        with open('keyword_tweets.json','a') as tf:
            tf.write(data)
        return True

    def on_error(self, status):
        print status

"""
----------------
T H E   L O O P
----------------
"""
# this is to that the script can be interrupted (ctrl+c)
try:
    while True:
        if __name__ == '__main__':

            #This handles Twitter authetification and the connection to Twitter Streaming API
            l = StdOutListener()
            auth = OAuthHandler(TwitterAuthKeywords.consumer_key, TwitterAuthKeywords.consumer_secret)
            auth.set_access_token(TwitterAuthKeywords.access_token, TwitterAuthKeywords.access_token_secret)
            stream = Stream(auth, l)

            #This line filter Twitter Streams to capture data by the keywords: 'architecture' etc.
            alltweets=stream.filter(track=keywords)

except KeyboardInterrupt:
    pass
