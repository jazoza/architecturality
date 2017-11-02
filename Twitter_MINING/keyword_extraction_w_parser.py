#!/usr/bin/env python
# encoding: utf-8

__author__      = "Naushad UzZaman (@naushadzaman)"

import os
import re
import sys
import string
import codecs
import subprocess

filepath = os.path.abspath(os.path.dirname(__file__))

reload(sys)
sys.setdefaultencoding('utf8')

from pattern.en import parse

stopwords = []
with open('twitter-sentiment-analysis-stopwords.txt','r') as s_file:
	for line in s_file.readlines():
		stopwords.append(line.strip())

### START Keyword extraction ###

def extract_link(text):
	regex = r'https?://[^\s<>"]+|www\.[^\s<>)"]+'
	match = re.findall(regex, text)
	links = []
	for x in match:
		if x[-1] in string.punctuation: links.append(x[:-1])
		else: links.append(x)
	return links

def cleanup(query):
	try:
		urls = extract_link(" " + query + " ")
		for url in urls:
			query = re.sub(url, "", query)
		q = query.strip()
	except:
		q = query
	q = re.sub(' RT ', '', ' ' + q + ' ').strip()
	return q


def convert_tag_format(query):
	word = query.split(' ')
	postag = [(x.split('/')[0], x.split('/')[1]) for x in word]
	return postag


def get_pos_tags(text):
	tagged_sent = parse(text)
	return convert_tag_format(tagged_sent), tagged_sent

def normalise(word):
	word = word.lower()
	return word


## conditions for acceptable word: length, stopword
def acceptable_word(word):
    accepted = bool(2 <= len(word) <= 12
        and word.lower() not in stopwords)
    return accepted

## extract entity from BIO encoding
def extract_entity(filetext):
	last_entity = ''
	last_tag = ''
	mention2entities = {}
	for line in filetext.split('\n'):
		line = line.strip()
		if line == '':
			continue
		line_split = line.split('\t')
		if re.search('B-', line_split[1]):
			if last_entity != '':
				if not last_tag in mention2entities:
					mention2entities[last_tag] = []
				mention2entities[last_tag].append(last_entity.strip())
			last_entity = line_split[0] + ' '
			last_tag = line_split[1][2:]
		elif re.search('I-', line_split[1]):
			last_entity += line_split[0] + ' '
	if last_entity != '':
		if not last_tag in mention2entities:
			mention2entities[last_tag] = []
		mention2entities[last_tag].append(last_entity.strip())
	return 	mention2entities


def get_entities_from_phrase(tagged_sent, phrase2consider):
	word = tagged_sent.split(' ')
	bio_tags = [normalise(x.split('/')[0])+ '\t'+ x.split('/')[2] for x in word]
	bio_text = '\n'.join(bio_tags)
	mention2entities = extract_entity(bio_text)
	print mention2entities.keys()

	## strip off unacceptable words
	_mention2entities = {}
	for mention in mention2entities:
		if not mention in phrase2consider:
			continue
		_mention2entities[mention] = []
		for entity in mention2entities[mention]:
			_entity = ' '.join([word for word in entity.split(' ') if acceptable_word(word)]).strip()
			if _entity != '':
				_mention2entities[mention].append(_entity)

	entities = []
	for mention in _mention2entities:
		entities.extend(_mention2entities[mention])
	return entities


def get_keywords(text, phrase2consider=['NP', 'ADJP']):
	_text = cleanup(text)
	try:
		postoks, tagged_sent = get_pos_tags(_text)
		entities = get_entities_from_phrase(tagged_sent, phrase2consider)
	except:
		return []
	return entities

### END Keyword extraction ###

### START other entity extraction ###
def extract_hashtag(text, to_normalize=True):
	regex = r'#[^\W\d_]+\b'
	if to_normalize: text = normalise(text)
	match = re.findall(regex, text)
	return match

def extract_users(text, to_normalize=True):
#	regex = r'@[^\W\d_]+\b'
	regex = r'@[^\b ]+\b'
	if to_normalize: text = normalise(text)
	match = re.findall(regex, text)
	return match


def get_emoji_list():
	emoji_text = codecs.open(filepath+'/emoji_table.txt', 'r', 'utf-8').read().split('\n')
	emojis = [x.split(',')[0] for x in emoji_text][1:]
	emojis = [x for x in emojis if x.strip() != '']
	return emojis
emojis = get_emoji_list()

def extract_emojis(text):
	global emojis
	_emos = []
	for each in emojis:
		each = each.strip()
		if each == '': continue
		if each in text:
			_emos.extend(re.findall(each, text.decode('utf-8')))

#	_emos2 = []
#	for char in text.decode('utf-8'):
#		if char in _emos:
#			_emos2.append(char)
	return _emos#, _emos2

### END other entity extraction ###

def all_entities(text, to_normalize=True, with_unigram=True):
	text = text.decode('utf-8')
	if to_normalize: text = normalise(text)
	if with_unigram:
		entities = text.split()
	else:
		entities = []
	keywords = get_keywords(text, ['NP', 'VP', 'ADJP', 'ADVP'])
	emojis = extract_emojis(text)
	for each in keywords+emojis:
		if not each in entities:
			entities.append(each)
	return entities

if __name__ == '__main__':
	queries = ["The mobile web is more important than mobile apps.", "As a #roadmapscholar, I highly recommend #startup bootcamp for #founders by @andrewsroadmaps : http://t.co/ZBISIMEBRH (http://t.co/VF5CojRWNF)", "RT @andrewsroadmaps: Proud of @naushadzaman &amp; @WasimKhal for winning the #IBMWatson hackathon! #roadmapscholars https://t.co/08sbAjKWKu."]

	for query in queries:
		print 'query', query
		print 'get_keywords(query)', get_keywords(query)
		print "get_keywords(query, ['NP'])", get_keywords(query, ['NP'])
		print "extract_hashtag(query)", extract_hashtag(query)
		print "extract_users(query)", extract_users(query)
		print "extract_link(query)", extract_link(query)
		print ''
