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
from preprocessing import tokenize, preprocess, stop

# load .csv files created by SCRAPING (comment out if using STREAMING collection)
#files = [f for f in listdir('.') if f.endswith('.csv') and isfile(join('.', f))]
#d = pd.concat([pd.read_csv(f) for f in files], keys=files)

# load .json files created by STREAMING (comment out if using the SCRAPING collection)
files = [f for f in listdir('.') if f.endswith('.json') and isfile(join('.', f))]
d = pd.concat([pd.read_json(f, lines=True) for f in files], keys=files)

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
