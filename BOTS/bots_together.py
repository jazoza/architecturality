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
import activeform_auth, contagiousarchi_auth, infosuperabundance_auth, digitalimmanence_auth, digitaltools_auth, stack_auth

#read in the theoretical texts
## Easterling, Extrastatecraft (active form)
activeformtext = [x.strip() for x in open('book_extrastatecraft.txt', 'r').readlines()]
activeform = '. '.join(activeformtext).decode('utf-8')
model_activeform = markovify.Text(activeform, state_size=1)
## Parisi, Contagious Archtecture (contagious architecture)
text = [x.strip() for x in open('book_contagious-architecture.txt', 'r').readlines()]
contagiousarch = '. '.join(text).decode('utf-8')
model_contagiousarch = markovify.Text(contagiousarch, state_size=1)
## McCullough, Ambient Commons
infosabundancetext = [x.strip() for x in open('book_information-superabundance.txt', 'r').readlines()]
superabundance = '. '.join(infosabundancetext).decode('windows-1252')
model_superabundance = markovify.Text(superabundance, state_size=1)
## Galloway, Laruelle (digital immanence)
digitimmanencetext = [x.strip() for x in open('book_digital-immanence.txt', 'r').readlines()]
digitimmanence = '. '.join(digitimmanencetext).decode('windows-1252')
model_digitimmanence = markovify.Text(digitimmanence, state_size=1)
## Kolarevic, Performatity (digital tools)
digittooltext = [x.strip() for x in open('book_digital-tools.txt', 'r').readlines()]
digitaltools = '. '.join(digittooltext).decode('utf-8')
model_digitaltools = markovify.Text(digitaltools, state_size=1)
## Bratton, Stack (stack)
stacktext = [x.strip() for x in open('book_stack.txt', 'r').readlines()]
stack = '. '.join(stacktext).decode('utf-8')
model_stack = markovify.Text(stack, state_size=1)


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
        return unicode('') # turn floats into empty strings

# generate a tweet
def atd(api,model,emphasis):
    files = [f for f in listdir('.') if f.endswith('.json') and isfile(join('.', f))] # list the collection files
    d = pd.concat([pd.read_json(f, lines=True) for f in files], keys=files) # load the tweets
    tweets_l = [parse_tweets_list(tweet) for tweet in d['text'].tolist()]
    text = '. '.join(tweets_l)
    model_tweets = markovify.Text(text, state_size=1)
    model_combo = markovify.combine([model_tweets,model],[1,emphasis])
    tweetTXT = model_combo.make_short_sentence(122)
    tweetWITHmention=tweetTXT+' '+mention(tweetTXT)
    print(tweetWITHmention)
    api.update_status(tweetWITHmention)

# friendly bots
friendlyBOTS = ['@active_form', '@contagiousarchi', '@infosabundance', '@digitalimmanent', '@digittools', '@a__stack']
def mention(tweet):
    # randomnumber = random.randint(0,20)
    # if randomnumber <= (len(friendlyBOTS)-1):
    #     account = friendlyBOTS[randomnumber]
    # else:
    #     account = ''
    # return account
    if 'form' or 'active' or 'urbanism' in tweet:
        mention = friendlyBOTS[0]
    elif 'thought' or 'soft' or 'prehension' in tweet:
        mention = friendlyBOTS[1]
    elif 'information' or 'abundance' or 'superabundance' in tweet:
        mention = friendlyBOTS[2]
    elif 'immanence' or 'immanent' in tweet:
        mention = friendlyBOTS[3]
    elif 'tool' or 'tools' or 'performativity' in tweet:
        mention = friendlyBOTS[4]
    elif 'layer' or 'stack' or 'earth' in tweet:
        mention = friendlyBOTS[5]
    elif 'digital' in tweet:
        mention = friendlyBOTS[random.choice([1,3,4])]
    else:
        mention = ''
    return mention
# the tweeting loop

try:
    while True:
        # run the tweet generating function
        atd(makeapi(activeform_auth),model_activeform,6)
        time.sleep(random.randint(20,200))
        atd(makeapi(contagiousarchi_auth),model_contagiousarch,3)
        time.sleep(random.randint(20,200))
        atd(makeapi(infosuperabundance_auth),model_superabundance,5)
        time.sleep(random.randint(20,200))
        atd(makeapi(digitalimmanence_auth),model_digitimmanence,4)
        time.sleep(random.randint(20,200))
        atd(makeapi(digitaltools_auth),model_digitaltools,15)
        time.sleep(random.randint(20,200))
        atd(makeapi(stack_auth),model_stack,2)
        time.sleep(random.randint(120,1200))
except KeyboardInterrupt:
    pass


# TO DO:
# put emphasis on some words - more likely than others (see markovify documentation)
# analyise interactions. for this to be interesting, there need to be a lot of interactions.
# click on the links, scrape web pages, scrape images from tweets
# Small LSTM Network to Generate Text for Alice in Wonderland
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.utils import np_utils
# load ascii text and covert to lowercase
filename = "BOTS/book_extrastatecraft.txt"
raw_text = open(filename).read()
raw_text = raw_text.lower()
# create mapping of unique chars to integers
chars = sorted(list(set(raw_text)))
char_to_int = dict((c, i) for i, c in enumerate(chars))
# summarize the loaded data
n_chars = len(raw_text)
n_vocab = len(chars)
# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []
for i in range(0, n_chars - seq_length, 1):
	seq_in = raw_text[i:i + seq_length]
	seq_out = raw_text[i + seq_length]
	dataX.append([char_to_int[char] for char in seq_in])
	dataY.append(char_to_int[seq_out])
n_patterns = len(dataX)
# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))
# normalize
X = X / float(n_vocab)
# one hot encode the output variable
y = np_utils.to_categorical(dataY)
# define the LSTM model
model = Sequential()
model.add(LSTM(256, input_shape=(X.shape[1], X.shape[2])))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
# define the checkpoint
filepath="weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
callbacks_list = [checkpoint]
# fit the model
model.fit(X, y, epochs=3, batch_size=128, callbacks=callbacks_list)
