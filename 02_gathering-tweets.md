# 02 | Gathering Tweets
Streaming tweets by 1)profile and 2)keywords.

Gathering the tweets is done using the [tweepy](https://github.com/tweepy/tweepy) module for authentication with the API and scraping or streaming of tweets.

## Authentication

Authentication is done using this code:

```python
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# User credentials to access Twitter API
access_token = "ACCESS TOKEN"
access_token_secret = "ACCESS TOKEN SECRET"
consumer_key = "CONSUMER KEY"
consumer_secret = "CONSUMER SECRET"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
```

The two gathering methods (by keyword and by profiles) are authenticating to two different apps - which had to be created so that I could simultaneously make the calls (interfering calls using the same auth would return 420 error on one streamer).

Scripts in this repository use an auth.py file where the credentials for all Twitter apps are stored. A model of this script is included in the repository, under the name `auth_model.py`.

## Scraping

Getting all the tweets from a particular user, or a list of users.
The [GET statuses/user timeline method](https://dev.twitter.com/rest/reference/get/statuses/user_timeline) is limited to the latest 3200 tweets by the Twitter API.
The script gets 200 initial tweets and then extends the list of `alltweets` to include the maximum number. Tweets are then stored in a .csv file, where *userID*, *tweet text* and *time of the tweet* are written line by line. The script stores separate files for each user.

## Streaming

Streaming is done by listening for specific **keywords** and to specific **profiles**, selected previously. The streamer class is created, and it opens a .json file to write the results

```python
class StdOutListener(StreamListener):

    def on_data(self, data):
        #print data
        with open('output.json','a') as tf:
            tf.write(data)
        return True

    def on_error(self, status):
        print status
```

The streamer is then running in a loop, listening to either keywords or profiles:

```python
try: # this is to that the script can be interrupted (ctrl+c)
    while True:
        if __name__ == '__main__':
            # Instantiate the StdOutListener
            l = StdOutListener()
            stream = Stream(auth, l)
            # Filter tweets by keyword
            alltweets=stream.filter(track=keywords)

except KeyboardInterrupt:
    pass
```
The only difference between the two streamers (apart from the app credentials) is the last line of code:

`alltweets=stream.filter(track=keywords)` for keyword streaming and  `stream.filter(follow=userID_list)` for profile streaming

Profile streaming requires the list of profiles to be converted from screen names to userIDs. This is done using the following script

**twythonize.py**
```python
from twython import Twython
from auth import TwitterAuthProfiles
import pickle

#Twython AUTHENTICATE (Oauth2)
#Obtain an OAuth 2 Access Token
twitter = Twython(TwitterAuthProfiles.consumer_key, TwitterAuthProfiles.consumer_secret, oauth_version=2)
ACCESS_TOKEN = twitter.obtain_access_token()
#Use the Access Token
twitter = Twython(TwitterAuthProfiles.consumer_key, access_token=ACCESS_TOKEN)

BIM_list=['profiles_appearing_in_search_for_BIM']
DynamoBIM_list=['profiles_appearing_in_search_for_DynamoBIM']
Revit_list=['profiles_appearing_in_search_for_revit']
DigArch_list=['profiles_appearing_in_search_for_digital_architecture']
Parametric_list=['profiles_appearing_in_search_for_parametric']
other_list=['other_relevant_profiles']
# adding a list of profiles who were tweeting the keywords from the second stream
keywords_list = []

#list of all lists
screen_names_list=list(set(BIM_list+DynamoBIM_list+Revit_list+DigArch_list+Parametric_list+other_list+keywords_list))
#Convert the list of Twitter screen names into a coma separated string, removing @signs into a string
screen_names_withoutat = []
for i in screen_names_list:
  screen_names_withoutat.append(i[1:])

# Query twitter with the comma separated list
userID_list = []
for user in screen_names_withoutat:
    userID=twitter.lookup_user(screen_name=user)
    userID_list.append(str(userID[0]["id_str"]))

# write the list of usedIDs to a file
with open('userID.txt', 'a') as f:
    pickle.dump(userID_list, f)
```

Each collection of tweets is stored in a .json file on the server, constantly updated. Tweets were collected: from `Fri, 31 Mar 2017 08:51:20.365 GMT` to `Wed, 12 Apr 2017 03:19:32.214 GMT` (profile_keywords.json, 20.5MB, 3632 tweets), from `Wed, 05 Apr 2017 12:58:49.914 GMT` to `Wed, 12 Apr 2017 02:55:44.893 GMT` (keyword_tweets.json, 126.4MB, 26994 tweets) and from `Thu, 30 Mar 2017 14:58:07.471 GMT` to `Fri, 31 Mar 2017 09:50:14.120 GMT` (keyword_SPOILED_tweets.json, 55.5MB). The *keyword* collection file is growing more quickly, but the *profile* collection seems to have more meaningful content.
