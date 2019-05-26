"""
import tweepy

#twitter application credentials
consumer_key="addYours"
consumer_secret="addYours"

#twitter user credentials
access_token="AddYours"
access_token_secret="AddYours"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

tweepyapi = tweepy.API(auth)

tweepyapi.update_status('Hello World!')
print("Hello " + tweepyapi.me().name)
"""

import tweepy

def get_api(cfg):
  auth = tweepy.OAuthHandler(cfg['consumer_key'], cfg['consumer_secret'])
  auth.set_access_token(cfg['access_token'], cfg['access_token_secret'])
  return tweepy.API(auth)

def main():
  # Fill in the values noted in previous step here
  cfg = { 
    "consumer_key"        : consumer_key,
    "consumer_secret"     : consumer_secret,
    "access_token"        : access_token,
    "access_token_secret" : access_token_secret 
    }

  api = get_api(cfg)
  tweet = "Hello, world!"
  status = api.update_status(status=tweet) 
  # Yes, tweet is called 'status' rather confusing

if __name__ == "__main__":
  main()
