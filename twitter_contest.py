import tweepy
from random import randint
import time

# This is a secret module containing oauth insanity tokens
# I got these following instructions at http://abhi74k.wordpress.com/2010/12/21/tweeting-from-python/
# If you wanted to use this script, you'd need to make the file secret_info.py, with each of the
# following variables containing the correct values
from secret_info import (consumer_key,
                         consumer_secret,
                         oauth_token_secret,
                         user_id,
                         oauth_token,
                         screen_name)

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(oauth_token, oauth_token_secret)
api = tweepy.API(auth)

print('Logged in as %s (id: %s)' % (screen_name, user_id))

print('%d API calls left this hour' % api.rate_limit_status()['remaining_hits'])

follower_cursors = tweepy.Cursor(api.followers, id=screen_name)
followers = [f.screen_name for f in follower_cursors.items()]

print('%d Followers' % len(followers))

# get the retweets for additional entries
tweets_cursor = tweepy.Cursor(api.user_timeline)
my_tweet_ids = [t.id for t in tweets_cursor.items()]

print('%d Tweets by me' % len(my_tweet_ids))

retweeters = []
for (i, tweet_id) in enumerate(my_tweet_ids):
    try:
        # I hate api limits...
        rate_limit_dict = api.rate_limit_status()
        if rate_limit_dict['remaining_hits'] < 5:
            print('Rate limit status = %d requests left.  Sleeping for 1 hour...')
            time.sleep(3605)

        # this assumes < 100 RT / tweet.  Thankfully not that famous... yet
        print("Processing retweets for tweet #%d..." % i)

        retweeters += [rt.author.screen_name for rt in api.retweets(tweet_id)]

    except tweepy.error.TweepError as e:
        print("an error occurred: %s" % e)


print('%d Retweeters' % len(retweeters))

candidates = followers + retweeters

draw = randint(0, len(candidates) - 1)

print('And the winner is: %s' % (candidates[draw]))
