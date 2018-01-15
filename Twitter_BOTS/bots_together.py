#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
---------------------
AUOMATE TWEETS USING MARKOVIFY MODULE
---------------------
"""
import tweepy, time, markovify, random, re, nltk, csv
import pandas as pd
from os import listdir
from os.path import isfile, join
import activeform_auth, contagiousarchi_auth, infosuperabundance_auth, digitalimmanence_auth, digitaltools_auth, stack_auth

# new markovify class, improved performance
class POSifiedText(markovify.Text):
    def word_split(self, sentence):
        words = re.split(self.word_split_pattern, sentence)
        words = [ "::".join(tag) for tag in nltk.pos_tag(words) ]
        return words

    def word_join(self, words):
        sentence = " ".join(word.split("::")[0] for word in words)
        return sentence

#read in the theoretical texts
## Easterling, Extrastatecraft (active form)
activeformtext = [x.strip() for x in open('book_extrastatecraft.txt', 'r').readlines()]
activeform = '. '.join(activeformtext)#.decode('utf-8') uncomment if running python 2
model_activeform = POSifiedText(activeform, state_size=1)
## Parisi, Contagious Archtecture (contagious architecture)
contagoiustext = [x.strip() for x in open('book_contagious-architecture.txt', 'r').readlines()]
contagiousarch = '. '.join(contagoiustext)#.decode('utf-8')
model_contagiousarch = POSifiedText(contagiousarch, state_size=1)
## McCullough, Ambient Commons
infosabundancetext = [x.strip() for x in open('book_information-superabundance.txt', 'r', encoding = "ISO-8859-1").readlines()]
superabundance = '. '.join(infosabundancetext)#.decode('windows-1252')
model_superabundance = POSifiedText(superabundance, state_size=1)
## Galloway, Laruelle (digital immanence)
digitimmanencetext = [x.strip() for x in open('book_digital-immanence.txt', 'r', encoding = "ISO-8859-1").readlines()]
digitimmanence = '. '.join(digitimmanencetext)#.decode('windows-1252')
model_digitimmanence = POSifiedText(digitimmanence, state_size=1)
## Kolarevic, Performatity (digital tools)
digittooltext = [x.strip() for x in open('book_digital-tools.txt', 'r').readlines()]
digitaltools = '. '.join(digittooltext)#.decode('utf-8')
model_digitaltools = POSifiedText(digitaltools, state_size=1)
## Bratton, Stack (stack)
stacktext = [x.strip() for x in open('book_stack.txt', 'r').readlines()]
stack = '. '.join(stacktext)#.decode('utf-8')
model_stack = POSifiedText(stack, state_size=1)


#authentications
def makeapi(authfile):
    auth = tweepy.OAuthHandler(authfile.TwitterAuth.consumer_key, authfile.TwitterAuth.consumer_secret)
    auth.set_access_token(authfile.TwitterAuth.access_token, authfile.TwitterAuth.access_token_secret)
    api = tweepy.API(auth)
    return api

# remove mentions and empty tweets
def parse_tweets_list(x):
    try:
        return re.sub(r'(?:@[\w_]+)', ' ', x) # remove mentions
    except TypeError:
        return ('') # turn floats into empty strings

# generate a tweet
def atd(api,model,emphasis,start):
    files = [f for f in listdir('.') if f.endswith('.json') and isfile(join('.', f))] # list the collection files
    d = pd.concat([pd.read_json(f, lines=True) for f in files], keys=files) # load the tweets
    tweets_l = [parse_tweets_list(tweet) for tweet in d['text'].tolist()]
    text = '. '.join(tweets_l)
    model_tweets = POSifiedText(text, state_size=1)
    model_combo = markovify.combine([model_tweets,model],[1,emphasis])
    tweetTXT = model_combo.make_sentence_with_start(start, strict=False, max_chars=220)
    tweetWITHmention=tweetTXT+' '+mention(tweetTXT)
    print(tweetWITHmention)
    api.update_status(tweetWITHmention)

# friendly bots
friendlyBOTS = ['@active_form', '@contagiousarchi', '@infosabundance', '@digitalimmanent', '@digittools', '@a__stack']
def mention(tweet):
    if ('form' or 'urbanism' or 'zone') in tweet:
        mention = friendlyBOTS[0]
    elif ('thought' or 'soft' or 'prehension' or 'architecture') in tweet:
        mention = friendlyBOTS[1]
    elif ('information' or 'abundance' or 'superabundance') in tweet:
        mention = friendlyBOTS[2]
    elif ('immanence' or 'against') in tweet:
        mention = friendlyBOTS[3]
    elif ('tool' or 'tools' or 'performativity') in tweet:
        mention = friendlyBOTS[4]
    elif ('user' or 'stack' or 'earth') in tweet:
        mention = friendlyBOTS[5]
    elif ('digital' or 'analog') in tweet:
        mention = friendlyBOTS[random.choice([1,3,4])]
    else:
        mention = ''
    return mention

# dictionary of accounts to choose from randomly
accounts_dict = [[activeform_auth,model_activeform,6,"active"], [contagiousarchi_auth,model_contagiousarch,3,"contagious"], [infosuperabundance_auth,model_superabundance,5,"atmospheric"],  [digitalimmanence_auth,model_digitimmanence,4,"immanent"], [digitaltools_auth,model_digitaltools,15,"digital"], [stack_auth,model_stack,2,"layer"]]

# Favorite, retweet
keywords = ['architects', 'architecture', 'autocad', 'autodesk', 'bim', 'building', 'concrete', 'construction', 'data', 'design', 'digital', 'engineering', 'future', 'housing', 'passivhaus', 'revit', 'tech', 'technology']

# the tweeting loop
try:
    while True:
        # run the tweet generating function
        choice = random.randint(0,5)
        try:
            atd(makeapi(accounts_dict[choice][0]),accounts_dict[choice][1],accounts_dict[choice][2],accounts_dict[choice][3])
            for word in keywords:
                for tweet in tweepy.Cursor(makeapi(accounts_dict[choice][0]).search,q=word+', '+accounts_dict[choice][3]).items(1):
                    try:
                        tweet.favorite()
                    except tweepy.TweepError as e:
                        print(e.reason)
        except tweepy.error.TweepError as e:
            print(e.reason)
            continue
        time.sleep(random.randint(10,200))
except KeyboardInterrupt:
    pass


# TO DO:
# put emphasis on some words - more likely than others (see markovify documentation)
# analyise interactions. for this to be interesting, there need to be a lot of interactions.
# click on the links, scrape web pages, scrape images from tweets
