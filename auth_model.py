class TwitterAuthKeywords:
# user credentials to access Twitter API for streaming keywords
	consumer_key="CONSUMER_KEY"
	consumer_secret="CONSUMER_SECRET"

	access_token="ACCESS_TOKEN"
	access_token_secret="ACCESS_TOKEN_SECRET"

class TwitterAuthProfiles:
# user credentials to access Twitter API for streaming profiles
	consumer_key="CONSUMER_KEY"
	consumer_secret="CONSUMER_SECRET"

	access_token="ACCESS_TOKEN"
	access_token_secret="ACCESS_TOKEN_SECRET"

"""
to test authentification, use the code below:
auth = tweepy.OAuthHandler(TwitterAuthProfiles.consumer_key, TwitterAuthProfiles.consumer_secret)
auth.set_access_token(TwitterAuthProfiles.access_token, TwitterAuthProfiles.access_token_secret)
api = tweepy.API(auth)
api.update_status('some text')
"""
