from tweepy import OAuthHandler, API, Cursor
from datetime import datetime, timedelta
from collections import Counter
from auth import TwitterAuthProfiles

auth = OAuthHandler(TwitterAuthProfiles.consumer_key, TwitterAuthProfiles.consumer_secret)
auth.set_access_token(TwitterAuthProfiles.access_token, TwitterAuthProfiles.access_token_secret)
auth_api = API(auth,
        # support for multiple authentication handlers
        # retry 3 times with 5 seconds delay when getting these error codes
        retry_count=3,retry_delay=5,retry_errors=set([401, 404, 500, 503]),
        # monitor remaining calls and block until replenished
        wait_on_rate_limit=True)


query = '#MAB18 OR #MAB16 OR #MAB14 OR #MAB12 OR #mediaarchitecture'
account_list = []
try:
    search_results = Cursor(auth_api.search, q=query).items(100)
except:
    print("some error")

for tweet in search_results:
    if tweet.user.id not in account_list:
        account_list.append(tweet.user.id)
    else:
        continue

if len(account_list) > 0:
  for target in account_list:
    print("Getting data for " + target)
    item = auth_api.get_user(target)
    print("name: " + item.name)
    print("screen_name: " + item.screen_name)
    print("description: " + item.description)
    print("statuses_count: " + str(item.statuses_count))
    print("friends_count: " + str(item.friends_count))
    print("followers_count: " + str(item.followers_count))

    tweets = item.statuses_count
    account_created_date = item.created_at
    delta = datetime.utcnow() - account_created_date
    account_age_days = delta.days
    print("Account age (in days): " + str(account_age_days))
    if account_age_days > 0:
      print("Average tweets per day: " + "%.2f"%(float(tweets)/float(account_age_days)))

    hashtags = []
    mentions = []
    tweet_count = 0
    end_date = datetime.utcnow() - timedelta(days=30)
    for status in Cursor(auth_api.user_timeline, id=target).items():
      tweet_count += 1
      if hasattr(status, "entities"):
        entities = status.entities
        if "hashtags" in entities:
          for ent in entities["hashtags"]:
            if ent is not None:
              if "text" in ent:
                hashtag = ent["text"]
                if hashtag is not None:
                  hashtags.append(hashtag)
        if "user_mentions" in entities:
          for ent in entities["user_mentions"]:
            if ent is not None:
              if "screen_name" in ent:
                name = ent["screen_name"]
                if name is not None:
                  mentions.append(name)
      if status.created_at < end_date:
        break

        print
    print("Most mentioned Twitter users:")
    for item, count in Counter(mentions).most_common(10):
      print(item + "\t" + str(count))

    print
    print("Most used hashtags:")
    for item, count in Counter(hashtags).most_common(10):
      print(item + "\t" + str(count))

    print
    print("All done. Processed " + str(tweet_count) + " tweets.")
    print
