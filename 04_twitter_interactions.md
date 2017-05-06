# 04 | Twitter interactions

According to Twitter documentation, this is the list of possible interactions:

### Definitions
* **App install attempts**: Clicks to install an app via the Tweet's Card
* **App opens**: Clicks to open an app via the Tweet's Card
* **Detail expands**: Clicks on the Tweet to view more details
* **Embedded media clicks**: Clicks to view a photo or video in the Tweet
* **Engagements**: Total number of times a user interacted with a Tweet. Clicks anywhere on the Tweet, including Retweets,replies, * follows, likes, links, cards, hashtags, embedded media, username, profile photo, or Tweet expansion
* **Engagement rate**: Number of engagements divided by impressions
* **Follows**: Times a user followed you directly from the Tweet
* **Hashtag clicks**: Clicks on hashtag(s) in the Tweet
* **Impressions**: Times a user is served a Tweet in timeline or search results
* **Leads submitted**: Times a user submitted his/her info via Lead Generation Card in the Tweet
* **Likes**: Times a user liked the Tweet
* **Link clicks**: Clicks on a URL or Card in the Tweet
* **Permalink clicks**: Clicks on the Tweet permalink (desktop only)
* **Replies**: Times a user replied to the Tweet
* **Retweets**: Times a user retweeted the Tweet
* **Shared via email**: Times a user emailed the Tweet to someone
* **User profile clicks**: Clicks on the name, @handle, or profile photo of the Tweet author

These interactions are documented in twitter report, which can be obtained from twitter analytics. It can be probably also discerned from @arhitekturality tweets metadata, which I have downloaded to a .json file (link to file)

## The bot

The text from tweets collected by SCRAPING user profiles is loaded into a dictionary of Markov chain models. These models are probability tables of words based on their appearance in the tweets.

```python
#create an empty dictionary for text models
files_dict = {}
#populate the dictionary with a model per .csv file
for i,textfile in enumerate(files):
    with open(textfile) as f:
        tweetcsv = csv.reader(f)
        tweetlist = []
        for row in tweetcsv:
            tweetlist.append(row[2])
        text = ','.join(tweetlist)
        model = markovify.Text(text)
        files_dict[files[i]]=model
```

From here, new tweets are generated in a loop, in a relatively irregular time interval (between 90s and 3minutes). This first experiment was running from 27. 02. 2017 at 10:51 to 14:52 (4 hours and 1 minute).

```python
#combine markov models into a combo; presence of each model determined by the associated number in the second argument list;
model_combo = markovify.combine([files_dict.values()[0],files_dict.values()[1],files_dict.values()[2],files_dict.values()[3],files_dict.values()[4],files_dict.values()[5],files_dict.values()[6],[1,1,1,1,1,1,1])

try:
    while True:
        tweetTXT = model_combo.make_short_sentence(140)
        print(tweetTXT)
        api.update_status(tweetTXT)
        time.sleep(random.randint(90,240))
except KeyboardInterrupt:
    pass
```
Generated tweets appeared quite well structured, grammatically correct and including all special types included in the original tweets - links, images (uploaded through twitter), hashtags and mentions. Mentions make a big percentage of all words used in tweets, however. All lines in text containing an "@" symbol make roughly 80% of all tweets (out of 1827 tweets only 353 don't include a mention). These tweets raised an immediate interest within the community, but this was unfortunately not due to the tweets content. One of the most common interactions with the bot's tweets was puzzlement about the reason one's account appeared in the tweet. This is a lucky coincidence of engagement, rather than a meaningful interaction, although all users that reacted to the bot's tweets, did so in a genuine way.

Note: Some time after the last check within this iteration (28.02.2017 at 16:50) the user @60secondrevit has blocked the @arhitekturality account from accessing its tweets.

### adapting the bot to keep updating, and remove @mentions

To avoid immediate dismissal of the bot's tweeets by the community, I decided to remove @mentions from the tweeted text and build up a base of interesting tweets, build a sort of a reputation on the platform. At the same time, I consider essential to be able to engage meaningfully with the user profiles, and for this a new tool needs to be developed.

The other important change was to keep updating the Markov chain model with incoming tweet. This meant repeatedly checking for tweets from the accounts I was listening to, and was the reason to switch from SCRAPING to STREAMING.

The bot was again tweeting in a relatively irregular interval (120 to 240s), from 27. 02. 2017 at 15:19 to 01. 03. 2017 at 08:47 (1 day, 17 hours and 28 minutes), and from  from 01.03.2017 at 14:44 to 03.03.2017 at 8:53. Incoming tweets Last time checked 28. 02. 2017 at 16:50.

The two interaction plots below demonstrate how the bot performed within the community, with @mentions at first and later without.

[Engagements, all (from 27. 02. 2017 at 10:51 to 01. 03. 2017 at 08:47), according to a .csv file downloaded from Twitter, plotted in reverse chronological order](engagements-ALL_d.png)

![Impressions, all (from 27. 02. 2017 at 10:51 to 01. 03. 2017 at 08:47), reverse chronological order (newest tweet first)](impressions-ALL_d.png)

In the second iteration of bot-tweeting, we can observe (see image XX) a strong decline in engagement rate, and even more so in engagements themselves - which means that even if tweets have been seen by an audience, they have not felt compelled to react to them.

### Third tweeting session, using STREAMED tweets

Loaded all collected tweets (keywords and profiles, gathered between 31st of March and 12th of April, and then again between 30th of April) into a dataframe; this gives me 43791; out of those 90 were empty
43701
