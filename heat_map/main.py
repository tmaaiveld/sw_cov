#!/usr/bin/env python3

from geopy.geocoders import Nominatim
import gmplot

import platform
import sys

# import twitter
import pandas as pd

import configparser
import argparse
import json

import twitter

# Read config file
Config = configparser.ConfigParser()
Config.read("./config.ini")

api = twitter.Twitter(
    auth = twitter.oauth.OAuth(
        Config.get("twitter", "access_token"),
        Config.get("twitter", "access_token_secret"),
        Config.get("twitter", "consumer_key"),
        Config.get("twitter", "consumer_secret")
    )
)
# Argument parser
parser = argparse.ArgumentParser(
     prog='PROG',
     formatter_class=argparse.RawDescriptionHelpFormatter,
     description=("""\
Twitter trend finder
  How to run?
  # search for specific trend e.g. coronavirus
  python main.py -q coronavirus
  # show 200 results (standard 100 is shown)
  python main.py -q coronavirus -c 200
  # run in verbose
  python main.py -q coronavirus -v
  # even more verbose
  python main.py -q coronavirus -vvv
"""))

parser.add_argument('-q',               help='Search query')
parser.add_argument('-c',               help='Search count')
parser.add_argument('--verbose', '-v',  help='Run in verbose', action='count')

args = parser.parse_args()

# declare standard values
# query
q = "coronavirus"
if args.q:
    q = args.q

# count
c = 2
if args.c:
    c = int(args.c)
# End of argument parser


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

if args.verbose >= 2:
    print(df)

# geo location
geolocator = Nominatim(user_agent="twitter-api")

coordinates = {'latitude': [], 'longitude': []}
for read_tweet in tweet:
    try:
        location = geolocator.geocode(tweet[read_tweet]['location'])

        # If coordinates are found for location
        if location:
            coordinates['latitude'].append(location.latitude)
            coordinates['longitude'].append(location.longitude)

    # If too many connection requests
    except:
        pass

gmap = gmplot.GoogleMapPlotter(30, 0, 3)
gmap.heatmap(coordinates['latitude'], coordinates['longitude'], radius=20)
gmap.draw("python_heatmap.html")
# end of geo location

df.to_csv("export.csv", sep='\t', encoding='utf-8')
