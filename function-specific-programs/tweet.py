"""
import tweepy

#twitter application credentials
consumer_key="knQFpTnjuSvr6OxYwebt3wyrd"
consumer_secret="Mhex3oRkmaF7lD3hoMvHpAD6ctW0ugKYCopTlhc0JzOLOMIZ0w"

#twitter user credentials
access_token="2846631344-wEozinvHfEIFxFVy51I6te8SrN5OTFtU00wxsiz"
access_token_secret="Nfx1U8a2TjAQXFLBrJIyy2p36sjBGAWFIthLc1cIoI56U"

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
    "consumer_key"        : "knQFpTnjuSvr6OxYwebt3wyrd",
    "consumer_secret"     : "Mhex3oRkmaF7lD3hoMvHpAD6ctW0ugKYCopTlhc0JzOLOMIZ0w",
    "access_token"        : "2846631344-wEozinvHfEIFxFVy51I6te8SrN5OTFtU00wxsiz",
    "access_token_secret" : "Nfx1U8a2TjAQXFLBrJIyy2p36sjBGAWFIthLc1cIoI56U" 
    }

  api = get_api(cfg)
  tweet = "Hello, world!"
  status = api.update_status(status=tweet) 
  # Yes, tweet is called 'status' rather confusing

if __name__ == "__main__":
  main()