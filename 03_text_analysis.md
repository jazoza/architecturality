# 03 | Tweets analysis

## Text

The first analysis on the text is made using the tweet text, which has been imported from the eight .csv files collected with the scraping script.

```python
from os import listdir
from os.path import isfile, join

files = [f for f in listdir('/path/to/files') if f.endswith('.csv') and isfile(join('/path/to/files', f))]
d = pd.concat([pd.read_csv(f) for f in files], keys=files)
# convert the text column from the dataframe to a string
tweets_l = d['text'].tolist() # create a list from 'text' column in d dataframe
```

## Preprocess the text of tweets

Separate in 'tokens', translate special characters and special expressions (emoticons), remove stopwords. Below are some basic preprocessing functions:

```python
import json, re, operator, string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
from nltk import bigrams

# with open('streaming.json', 'r') as f:
#     line = f.readline() # read only the first tweet/line
#     tweet = json.loads(line) # load it as Python dict
#     print(json.dumps(tweet, indent=4)) # pretty-print

"""
word count, using nltk.corpus stopwords
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
```
Finally, preprocess the tweet text and create a string of tweet words to analyse for word frequency and keywords.
```python
tweets = '' # tweets are an empty string
for item in tweets_l:
  terms_only = [term for term in preprocess(unicode(item, errors='ignore')) if term not in stop and not term.startswith(('#', '@', 'http'))]
  for terms in terms_only:
    tweets = tweets + ' ' + terms # append each tweet after each other as a unicode string
```

## Wordcloud

Create a wordcloud from the list of tweets created with the above process. Using the [wordcloud library](https://github.com/amueller/word_cloud) by [Andreas Mueller](https://github.com/amueller)

```python
from wordcloud import WordCloud
import matplotlib.pyplot as plt
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
```
Generates this image:
![Wordcloud of tweets collected from the list of eight profiles, all (from 27. 02. to 28. 02. 2017)](wordcloud_02-28-2017_preprocessed.png)

## Keywords extraction

Extracting keywords from the list of tweets created with the above process. Using a [Python implementation of the Rapid Automatic Keyword Extraction (RAKE) algorithm] (https://github.com/zelandiya/RAKE-tutorial)

```python
import rake, operator
rake_object = rake.Rake("SmartStoplist.txt", 4, 2, 4) # words of minimum length 4, in groups of maximum 2, appearing at least 3 times in the text; this happens to give the best results with the particular corpus

keywords = rake_object.run(tweets)
#write the list of tuples to a file:
outfile = open('keywords_tweets_extractedkwords.txt', 'w')
for item in keywords:
  keyword = item[0]
  relevance = item[1]
  try:
    outfile.write(str(keyword.decode('utf-8'))+' '+str(relevance)+'\n')
  except UnicodeEncodeError:
    outfile.write(str(keyword)+' '+str(relevance)+'\n')
```
Results are not that convincing and do not reflect the word frequency represented before

`strategy motivation 4.0
followers usa 4.0
followers spain 4.0
free map 3.875
wanna call 3.77380952381
posted photo 3.76470588235
blog post 3.76050591595
find files 3.44957983193
files find 3.44957983193
daily build 3.41025641026
architecture license 3.32941176471
creative work 3.26612903226
architect podcast 3.15503875969
post 1.80701754386
architecture 1.8
nodes 1.77777777778
data 1.76923076923
posted 1.76470588235
show 1.75
design 1.75
find 1.73529411765
building 1.72413793103
read 1.72
part 1.71428571429
list 1.70588235294
projects 1.69230769231
sounds 1.69230769231
space 1.6875
hear 1.6875
future 1.6875
class 1.6875
today 1.68518518519
node 1.68421052632
join 1.68421052632
tools 1.67741935484
check 1.67441860465
code 1.66666666667
podcast 1.66666666667
revit 1.66666666667
twitter 1.66666666667
great 1.66666666667
live 1.66666666667
tool 1.66666666667
coming 1.65517241379
happy 1.65
people 1.64864864865
humans 1.63636363636
missed 1.63636363636
printed 1.63636363636
make 1.62962962963
workshop 1.625
dynamo 1.6170212766
watch 1.61538461538
thinking 1.61111111111
start 1.60714285714
back 1.60714285714
send 1.6
`

## Downloading all images (media) from collected tweets

```python
import urllib
import pandas as pd

df=pd.read_json('profile_tweets.json', lines=True)

for label, value in df_profile.entities.iteritems(): # iterate through the dictionary of entities
  if type(value)==dict and 'media' in value.keys(): # some value.keys are nan, and their type is 'float'
    for thing in value['media']:
      urllib.urlretrieve(thing['media_url'],'%s.jpg' %label) # save all images with the unique of their index in the df
```
