#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Extracts keywords from a collection of tweets
# works with both streaming and scraping methods (for difference, see 02_gathering-tweets.md)

import pandas as pd
from os import listdir
from os.path import isfile, join
import json, re, operator, string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk import bigrams
import preprocessing
import rake
import keyword_extraction_w_parser

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
        terms_only = [term for term in preprocessing.preprocess(item) if term not in stop and not term.startswith(('@', 'http'))]
        for terms in terms_only:
            tweets = tweets + ' ' + terms
        tweets = tweets + '.' # add an endstop to the end of each tweet (item) for keyword extraction
