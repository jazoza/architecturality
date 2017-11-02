#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
---------------------
AUOMATE TWEETS USING MARKOVIFY MODULE
---------------------
"""
import tweepy, time, markovify, random, re, csv
import pandas as pd
from os import listdir
from os.path import isfile, join
from auth import TwitterAuthProfiles

auth = tweepy.OAuthHandler(TwitterAuthProfiles.consumer_key, TwitterAuthProfiles.consumer_secret)
auth.set_access_token(TwitterAuthProfiles.access_token, TwitterAuthProfiles.access_token_secret)
api = tweepy.API(auth)

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
    text = '. '.join(tweets_l)
    model = markovify.Text(text)
    tweetTXT = model.make_short_sentence(140)
    print(tweetTXT)
    api.update_status(tweetTXT)

# SCRAPED TWEETS
# the tweeting function
"""
def atd():
    files = [f for f in listdir('.') if f.endswith('.csv') and isfile(join('.', f))] # reload the files
    #create an empty dictionary for text models
    files_dict = {}
    #populate the dictionary with a model per csv file
    for i,textfile in enumerate(files):
        with open(textfile) as f:
            tweetcsv = csv.reader(f)
            # create an empty list of tweets (texts)
            tweetlist = []
            for row in tweetcsv:
                # split the tweet text (row[2]) into words to eliminate mentions
                words = row[2].split()
                newwords = []
                for word in words:
                    if not word.startswith("@"):
                        newwords.append(word)
                # create a string from remaining words in a tweet
                newrow = ' '.join(newwords)
                # populate the list of tweets
                tweetlist.append(newrow)
            # convert the list to a string, for markovify model
            text = ','.join(tweetlist)
            model = markovify.Text(text)
            files_dict[files[i]]=model
    # combine markov models into a combo; presence of each model determined by the associated number in the second argument list; manually insert the number of files according to len(files_dict)
    model_combo = markovify.combine([ files_dict.values()[0], files_dict.values()[1], files_dict.values()[2], files_dict.values()[3], files_dict.values()[4], files_dict.values()[5], files_dict.values()[6], files_dict.values()[7], files_dict.values()[8] ], [ 1, 1, 1, 1, 1, 1, 1, 1, 1 ])
    tweetTXT = model_combo.make_short_sentence(140)
    print(tweetTXT)
    api.update_status(tweetTXT)
"""

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
