# Architecturality: How Space is Organised by Computation

The presented research explores how the challenge of organising a discourse that addresses computational process in architectural design could be delegated to computation. A lot of the interesting discussion about computational design today happens in social media as it does in the academic discourse. With the interest in unobserved connections and manifestations of digital processes, we value the immediacy of the social media discourse, as well as its limited reflectivity. How can we uncover and organise inherent qualities of computation in architectural experiences? How could we describe computational ideas in the language of design, and vice versa?

This repository documents the different steps taken in the exploration of the activity in social networks by a community of designers, architects and engineers who actively talk about computer-aided and data-driven design, simulation, computer-aided manufacturing and occupancy evaluation tools. The code relies on existing open source tools such as Python tweepy, facebook, textmining, markovify and sompy modules in combination with Twitter and Facebook Graph APIs. The work is divided in steps which occurred sequentially as well as informing each other continuously. The aforementioned tools are used to design the activity of programmed accounts (bots) which talk back and engage with the community. This act of talking, according to specifically programmed rules is an act of modeling the discourse. We intend to observe the way other avatars (belonging to humans as well as to other bots) will engage with it and study their interactions.

## 01. selecting the community
Gathering lists of Twitter profiles. Filtering users according to their profile descriptions, searching for keywords. Keywords are constantly updated according to results.

## 02. gathering tweets
Streaming tweets by 1)profile and 2)keywords. Created two Twitter apps which are used to authenticate two Python tweepy listeners at the same time, listening to a set of keywords [*twitter_streaming_keywords.py*] (identified in a qualitative manner) and a set of profiles [*twitter_streaming_profiles.py*] (identified in the previous step). The script listening to tweets from profile lists requires first the list of screen names to be converted to their IDs, which is done with the [*twythonize_list.py*] script.

## 03. first text analysis (keywords, word frequencies)
Using different tools to identify keywords, word frequencies and other regularities in the collection.

## 04. talking back, twitter interactions
Using the corpus of collected tweets to tweet back to the community. Tweeting "back" means using screen names and hashtags that are characteristic to this loosely defined community. Observing the interactions.

--

Chair for Architectural Theory and Philosophy of Technics, Institute For Architectural Sciences, TU Vienna
Febraury 2017
