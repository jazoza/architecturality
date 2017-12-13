from itertools import chain
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist
from collections import Counter
from nltk import bigrams

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
        tokens = [token if emoticon_re.search(token) else token for token in tokens]
    return tokens

#stopwords
with open("Twitter_MINING/twitter-sentiment-analysis-stopwords.txt", 'rb') as f:
    twitterstop = [str(word.strip()) for word in f.readlines()]
stop = stopwords.words('english') + list(string.punctuation) + twitterstop


#load the posts
with open("dezeentech_allposts.txt", "rb") as d:
    dezeenpoststxt = ('').join(d.readlines())
wordlist = dezeenpoststext.split()
wordlist_lower = [x.lower() for x in wordlist]

"""
----------------
WORD FREQUENCY
----------------
"""
#Count All words
total_words = len(wordlist_lower)
print('Total number of words in the collection: ', total_words)

# remove stop and other words (stemming)
porter = nltk.PorterStemmer()
meaningful_list = [porter.stem(term) for term in wordlist_lower if term not in stop and not term.startswith('http') and len(term)>2]
print('Total number of meaningful words (without stopwords): ', len(meaningful_list))

# Count terms only once, equivalent to Document Frequency
terms_single = set(meaningful_list)
print('Number of unique terms: ', len(terms_single))

# Count terms only (no hashtags, no mentions)
terms_only = [term for term in meaningful_list if not term.startswith('#') and not term.startswith('@')]
print('The number of unique terms only (no hashtags, no mentions): ', len(set(terms_only)))

#Word frequency for all terms (including hashtags and mentions)
wordfreq = FreqDist(meaningful_list)
print('The 200 most frequent terms, including special terms: ', wordfreq.most_common(200))

# Word frequency for terms only (no hashtags, no mentions)
termonlyfreq = FreqDist(terms_only)
print('The 200 most frequent terms (terms only): ', termonlyfreq.most_common(200))

# Count hashtags only
terms_hash = [term for term in meaningful_list if term.startswith('#')]
print('List and total number of hashtags: ', set(terms_hash), len(set(terms_hash)))

# Count mentions only
terms_mention = [term for term in meaningful_list if term.startswith('@')]
print('List and total number of mentions: ', set(terms_mention), len(set(terms_mention)))

# Mentions and Hashtags frequency
mentionsfreq = FreqDist(terms_mention)
print(mentionsfreq.most_common(100))
hashfreq = FreqDist(terms_hash)
print(hashfreq.most_common(100))

""" PLOT RESTULTS """

import numpy as np
import matplotlib.pyplot as plt

popularwords = termonlyfreq.most_common(100)

labels, values = zip(*popularwords.items())
# sort your values in descending order
indSort = np.argsort(values)[::-1]
# rearrange your data
labels = np.array(labels)[indSort]
values = np.array(values)[indSort]
indexes = np.arange(len(labels))
bar_width = 0.35
plt.bar(indexes, values)
# add labels
plt.xticks(indexes + bar_width, labels)
plt.show()

# author_names = counter.keys()
# author_counts = counter.values()
#
# # Plot histogram using matplotlib bar().
# indexes = np.arange(len(author_names))
# width = 0.7
# plt.bar(indexes, author_counts, width)
# plt.xticks(indexes + width * 0.5, author_names)
# plt.show()


"""
----------------
N - GRAMS
----------------
"""
def find_ngrams(input_list, n):
  return zip(*[input_list[i:] for i in range(n)])

find_ngrams(wordlist, 3)
