import tweepy, csv, time
from auth import TwitterAuthProfiles

#authorize twitter, initialize tweepy
auth = tweepy.OAuthHandler(TwitterAuthProfiles.consumer_key TwitterAuthProfiles.consumer_secret)
auth.set_access_token(TwitterAuthProfiles.access_token TwitterAuthProfiles.access_token_secret)
api = tweepy.API(auth)

# list of accounts that the stream is listening to
atd_list = ["ProvingGroundIO","Parametric01","archinate","digitag","andydeutsch","BjarkeIngels","etroxel","ColinMcCrone","iperezarnal","60secondrevit"]

def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	#initialize a list to hold all the tweepy Tweets
	alltweets = []
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200)
	#save most recent tweets
	alltweets.extend(new_tweets)
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print "getting tweets before %s" % (oldest)
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		#save most recent tweets
		alltweets.extend(new_tweets)
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		print "...%s tweets downloaded so far" % (len(alltweets))
	#transform the tweepy tweets into a 2D array that will populate the csv
    # inlcudes only user id, timestamp and text of a tweet
	outtweets = [[tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	#write the csv
    # creates a separate file for each account in the atd_list
	with open('%s_tweets.csv' % screen_name, 'a') as f: # open with 'w' writes and with 'a' it appends to existing file
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text"])
		writer.writerows(outtweets)
	pass

try: # allow the script to be interrupted manually (ctrl+c)
	while True:
		if __name__ == '__main__':
			#pass in the username of the account you want to download
			for account in atd_list:
				get_all_tweets(account)
		time.sleep(240)
except KeyboardInterrupt:
    pass
