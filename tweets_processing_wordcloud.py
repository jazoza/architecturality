#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Generate a wordcloud from a collection of tweets
# works with both streaming and scraping methods (for difference, see 02_gathering-tweets.md)

import pandas as pd
from os import listdir
from os.path import isfile, join
import json, re, operator, string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk import bigrams
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# load .csv files created by SCRAPING (comment out if using STREAMING collection)
#files = [f for f in listdir('.') if f.endswith('.csv') and isfile(join('.', f))]
#d = pd.concat([pd.read_csv(f) for f in files], keys=files)

# load .json files created by STREAMING (comment out if using the SCRAPING collection)
files = [f for f in listdir('.') if f.endswith('.json') and isfile(join('.', f))]
d = pd.concat([pd.read_json(f, lines=True) for f in files], keys=files)

"""
-----------------------
preprocessing functions
-----------------------
"""
emoticons_str = r"""
    (?:
        [:=;] # Eyes
        [oO\-]? # Nose (optional)
        [D\)\]\(\]/\\OpP] # Mouth
    )"""

regex_str = [
    emoticons_str,
    r'<[^>]+>', # HTML tags
    r'(?:@[\w_]+)', # @-mentions
    r"(?:\#+[\w_]+[\w\'_\-]*[\w_]+)", # hash-tags
    r'http[s]?://(?:[a-z]|[0-9]|[$-_@.&amp;+]|[!*\(\),]|(?:%[0-9a-f][0-9a-f]))+', # URLs

    r'(?:(?:\d+,?)+(?:\.?\d+)?)', # numbers
    r"(?:[a-z][a-z'\-_]+[a-z])", # words with - and '
    r'(?:[\w_]+)', # other words
    r'(?:\S)' # anything else
]

tokens_re = re.compile(r'('+'|'.join(regex_str)+')', re.VERBOSE | re.IGNORECASE)
emoticon_re = re.compile(r'^'+emoticons_str+'$', re.VERBOSE | re.IGNORECASE)

def tokenize(s):
    return tokens_re.findall(s)

def preprocess(s, lowercase=False):
    tokens = tokenize(s)
    if lowercase:
        tokens = [token if emoticon_re.search(token) else token.lower() for token in tokens]
    return tokens

punctuation = list(string.punctuation)
stop = stopwords.words('english') + punctuation + ['RT', 'The', 'rt', 'via', 'amp']

"""
-----------------------
preprocessing the tweets
converting to a string
-----------------------
"""
# convert the text column from the dataframe to a string
tweets_l = d['text'].tolist() # create a list from 'text' column in d dataframe
tweets = '' # tweets are an empty string
for item in tweets_l:
    if not isinstance(item, float): # check if the tweet text is not empty (appears as 'float')
        # for SCRAPED tweets (str)
        #terms_only = [term for term in preprocess(unicode(item, errors='ignore')) if term not in stop and not term.startswith(('@', 'http'))]
        # for STREAMED tweets (unicode)
        terms_only = [term for term in preprocess(item) if term not in stop and not term.startswith(('@', 'http'))]
        for terms in terms_only:
            tweets = tweets + ' ' + terms

"""
-----------------------
wordcloud generation
-----------------------
"""
# specify fonts, stopwords, background color and other options
wordcloud = WordCloud(font_path='/Users/zoza/Library/Fonts/CooperHewitt-Bold.otf',
                          stopwords=open('twitter-sentiment-analysis-stopwords.txt').read().split(),
                          background_color='white',
                          width=2400,
                          height=2000
                         ).generate(tweets)


plt.imshow(wordcloud)
plt.axis('off')
plt.show()
