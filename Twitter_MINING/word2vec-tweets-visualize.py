import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
from nltk.tokenize import word_tokenize
import gensim
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt


# load the tweets
tweets_df = pd.read_json('../Twitter_SCRAPING/profile_tweets.json', lines=True)

# drop columns that will not be used in analysis
tweets_df.drop(['contributors', 'coordinates', 'created_at', 'delete', 'display_text_range', 'entities', 'extended_tweet', 'retweet_count', 'retweeted', 'favorite_count', 'favorited', 'truncated', 'id_str', 'in_reply_to_status_id_str', 'in_reply_to_user_id_str', 'quoted_status_id_str','geo'],axis=1,inplace=True)

# drop rows with empty tweet.text
tweets_df.dropna(how='all', inplace=True)
tweets_df.reset_index(drop=True,inplace=True)

# text cleaning function:
'''
1. Souping / resolve problems with HTML encoding
2. BOM (Byte Order Mark) removing / in py2 solved by decoding to utf-8-sig; in py3 simply replace the characters
3. negation handling (replace key with values from negation_dic)
4. lower-case
5. removing special characters
6. tokenizing and joining
'''

pat1 = r'@[A-Za-z0-9_]+'
pat2 = r'https?://[^ ]+'
#combined_pat = r'|'.join((pat1, pat2))
www_pat = r'www.[^ ]+'
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}
neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

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

def tweet_cleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    try:
        bom_removed = souped.replace(u"\ufffd", "?")
    except:
        bom_removed = souped
    neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], bom_removed).lower()
    words = [x for x  in preprocess(neg_handled) if len(x) > 1 and not x.startswith(':')]
    return (" ".join(words)).strip()

# further text cleeaning: no mentions, no urls and no hashtags
pat1 = r'@[A-Za-z0-9_]+' # mention
pat2 = r'https?://[^ ]+' # url
combined_pat = r'|'.join((pat1, pat2))
www_pat = r'www.[^ ]+'
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not"}
neg_pattern = re.compile(r'\b(' + '|'.join(negations_dic.keys()) + r')\b')

def tweet_cleaner_further(text):
    stripped = re.sub(combined_pat, '', text)
    stripped = re.sub(www_pat, '', stripped)
    letters_only = re.sub("[^a-zA-Z]", " ", stripped)
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = [x for x  in tokenize(letters_only) if len(x) > 1 and not x.startswith('#')]
    return (" ".join(words)).strip()

# clean the tweets, create a list of clean tweets (one for first cleaning function and the other for tweets with mentions, urls and hashtags removed)
clean_tweet_texts = []
for i in range(0,len(tweets_df)):
    if( (i+1)%1000 == 0 ):
        print("Tweets", i+1, "of ", len(tweets_df), "has been processed")
    clean_tweet_texts.append(tweet_cleaner(tweets_df['text'][i]))

cleaner_tweet_texts = []
for i in range(0,len(clean_tweet_texts)):
    if( (i+1)%1000 == 0 ):
        print("Tweets", i+1, "of ", len(clean_tweet_texts), "has been processed")
    cleaner_tweet_texts.append(tweet_cleaner_further(clean_tweet_texts[i]))

# create a new df from cleaned tweets and original columns
clean_df = pd.DataFrame(np.column_stack([clean_tweet_texts, cleaner_tweet_texts]),
                               columns=['text1', 'text2'])

clean_df['timestamp'] = tweets_df.timestamp_ms
clean_df['location'] = tweets_df.place
clean_df['lang'] = tweets_df.lang
clean_df['extra'] = tweets_df.extended_entities
#clean_df.to_csv('clean_tweet.csv',encoding='utf-8')
print('clean_df', len(clean_df))

# only english tweets
english_df = clean_df[clean_df.lang == 'en']
print('english_df', len(english_df))

#####################################################
# word2 vec model

# X is a list of tokenized texts (i.e. list of lists of tokens)
X = [word_tokenize(item) for item in english_df['text2'].tolist()]
#print(X[0:3])
model = gensim.models.Word2Vec(X, iter=5, min_count=6, size=100) # min_count: how many times a word appears in the corpus
print(len(model.wv.vectors))

# USING TSNE TO DISPLAY SIMILAR WORDS IN THE WORD2VEC MODEL
# https://medium.com/@aneesha/using-tsne-to-plot-a-subset-of-similar-words-from-word2vec-bb8eeaea6229

# display model funciton
def display_closestwords_tsnescatterplot(model, word):

    arr = np.empty((0,100), dtype='f')
    word_labels = [word]

    # get close words
    close_words = model.wv.most_similar(positive=[word], topn=12)

    # add the vector for each of the closest words to the array
    arr = np.append(arr, np.array([model.wv[word]]), axis=0)
    for wrd_score in close_words:
        wrd_vector = model.wv[wrd_score[0]]
        word_labels.append(wrd_score[0])
        arr = np.append(arr, np.array([wrd_vector]), axis=0)

    # find tsne coords for 2 dimensions
    tsne = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    Y = tsne.fit_transform(arr)

    x_coords = Y[:, 0]
    y_coords = Y[:, 1]
    # display scatter plot
    plt.scatter(x_coords, y_coords)

    for label, x, y in zip(word_labels, x_coords, y_coords):
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    plt.xlim(x_coords.min()+0.00005, x_coords.max()+0.00005)
    plt.ylim(y_coords.min()+0.00005, y_coords.max()+0.00005)
    plt.show()

word_to_compare = input('please type in a word to compare with: ')
display_closestwords_tsnescatterplot(model, word_to_compare)
