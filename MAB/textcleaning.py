# text cleaning function:
'''
1. Souping / resolve problems with HTML encoding
2. BOM (Byte Order Mark) removing / in py2 solved by decoding to utf-8-sig; in py3 simply replace the characters
3. negation handling (replace key with values from negation_dic)
4. lower-case
5. removing special characters
6. tokenizing and joining
'''
import re
from bs4 import BeautifulSoup

pat1 = r'@[A-Za-z0-9_]+'
pat2 = r'https?://[^ ]+'
combined_pat = r'|'.join((pat1, pat2))
www_pat = r'www.[^ ]+'
negations_dic = {"isn't":"is not", "aren't":"are not", "wasn't":"was not", "weren't":"were not",
                "haven't":"have not","hasn't":"has not","hadn't":"had not","won't":"will not",
                "wouldn't":"would not", "don't":"do not", "doesn't":"does not","didn't":"did not",
                "can't":"can not","couldn't":"could not","shouldn't":"should not","mightn't":"might not",
                "mustn't":"must not","c'mon":"come on"}
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

def textCleaner(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    try:
        bom_removed = souped.replace(u"\ufffd", "?")
    except:
        bom_removed = souped
    neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], bom_removed).lower()
    words = [x for x  in preprocess(neg_handled) if len(x) > 1 and not x.startswith(':') and not x[0].isdigit()]
    return (" ".join(words)).strip()

def textCleanerFurther(text):
    stripped = re.sub(combined_pat, '', text)
    stripped = re.sub(www_pat, '', stripped)
    letters_only = re.sub("[^a-zA-Z]", " ", stripped)
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = [x for x  in tokenize(letters_only) if len(x) > 1 and not x.startswith('#')]
    return (" ".join(words)).strip()

def textCleanLinks(text):
    soup = BeautifulSoup(text, 'lxml')
    souped = soup.get_text()
    try:
        bom_removed = souped.replace(u"\ufffd", "?")
    except:
        bom_removed = souped
    neg_handled = neg_pattern.sub(lambda x: negations_dic[x.group()], bom_removed).lower()
    stripped = re.sub(pat2, '', neg_handled)
    stripped = re.sub(www_pat, '', stripped)
    letters_only = re.sub("[^a-zA-Z]", " ", stripped)
    # During the letters_only process two lines above, it has created unnecessay white spaces,
    # I will tokenize and join together to remove unneccessary white spaces
    words = [x for x  in tokenize(letters_only) if len(x) > 1]
    return (" ".join(words)).strip()
