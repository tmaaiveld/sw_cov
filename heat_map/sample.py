#!/usr/bin/env python3
import pandas as pd
import json
import twitter
import pyarrow.parquet as pq


# Read config file
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = '' 
OAUTH_TOKEN_SECRET = ''

api = twitter.Twitter(
    auth = twitter.oauth.OAuth(
        OAUTH_TOKEN, OAUTH_TOKEN_SECRET,CONSUMER_KEY, CONSUMER_SECRET
    )
)

q = "coronavirus"
c = 100



results =  api.search.tweets(q=q, count=c)
statuses = results['statuses']

j = 0
tweet = {}
for i, status in enumerate(statuses):
    if status['user']['geo_enabled'] and len(status['user']['location'])!=0:
        if args.verbose:
            print(json.dumps(status, indent=4, sort_keys=True))
        tweet[j]                   = {}
        tweet[j]['id']             = status['id']
        tweet[j]['location']       = status['user']['location']
        tweet[j]['place']          = status['place']
        tweet[j]['retweet_count']  = status['retweet_count']
        tweet[j]['text']           = status['text']
        tweet[j]['username']       = status['user']['name']
        tweet[j]['created_at']     = status['created_at']
        j += 1

df = pd.DataFrame.from_dict(tweet).T

df.to_parquet('export_'+str(q)+'.parquet')
