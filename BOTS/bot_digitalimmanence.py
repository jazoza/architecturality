#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
---------------------
AUOMATE TWEETS USING MARKOVIFY MODULE (DIGITAL IMMANENCE)
---------------------
"""
import tweepy, time, markovify, random, re, csv
import pandas as pd
from os import listdir
from os.path import isfile, join
from digitalimmanence_auth import TwitterAuth

auth = tweepy.OAuthHandler(TwitterAuth.consumer_key, TwitterAuth.consumer_secret)
auth.set_access_token(TwitterAuth.access_token, TwitterAuth.access_token_secret)
api = tweepy.API(auth)


#read in the theoretical text
text = [x.strip() for x in open('digital-immanence.txt', 'r').readlines()]
digitimmanence = '. '.join(text)
model_digitimmanence = markovify.Text(digitimmanence, state_size=1)
#STREAMING tweets
# remove mentions and empty tweets
def parse_tweets_list(x):
    try:
        return re.sub(r'(?:@[\w_]+)', ' ', x) # remove mentions
    except TypeError:
        return unicode('') # turn floats into empty strings

# generate a tweet
def atd():
    files = [f for f in listdir('.') if f.endswith('.json') and isfile(join('.', f))] # list the collection files
    d = pd.concat([pd.read_json(f, lines=True) for f in files], keys=files) # load the tweets
    tweets_l = [parse_tweets_list(tweet) for tweet in d['text'].tolist()]
    text = '. '.join(tweets_l).encode('utf-8')
    model_tweets = markovify.Text(text, state_size=1)
    model_combo = markovify.combine([model_tweets,model_digitimmanence],[1,6])
    tweetTXT = model_combo.make_short_sentence(130)
    tweetWITHmention=tweetTXT+' '+mention()
    print(tweetWITHmention)
    api.update_status(tweetWITHmention)

# friendly bots
friendlyBOTS = ['@active_form', '@contagiousarchi', '@infosabundance', '@digittools', '@a__stack']
def mention():
    randomnumber = random.randint(0,20)
    if randomnumber <= 4:
        account = friendlyBOTS[randomnumber]
    else:
        account = ''
    return account

# the tweeting loop

try:
    while True:
        atd() # run the tweet generating function
        time.sleep(random.randint(120,1200))
except KeyboardInterrupt:
    pass


# TO DO:
# put emphasis on some words - more likely than others (see markovify documentation)
# analyise interactions. for this to be interesting, there need to be a lot of interactions.
# click on the links, scrape web pages, scrape images from tweets
