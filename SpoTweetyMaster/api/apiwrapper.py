# encoding=utf8
from twython import Twython, TwythonError
from collections import defaultdict
import re
from django.conf import settings
import requests
import json


class TCOL(object):

    def __init__(self):
        super(TCOL, self).__init__()

    @staticmethod
    def get_topsongs(location):
        # DEFINE KEYS FROM SETTINGS------------------------------------------------------#
        #FORMAT = "json"
        APP_KEY = settings.APP_KEY
        APP_SECRET = settings.APP_SECRET
        #geocode_val = '41.015137,28.979530,1000km'  # latitude,longitude,distance(mi/km)
        geocode_val = location# latitude,longitude,distance(mi/km)

        # Create Twython Objects---------------------------------------------------------#
        twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)
        ACCESS_TOKEN = twitter.obtain_access_token()
        twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

        # Create Program Objects---------------------------------------------------------#
        MAX_ATTEMPTS = 5000
        COUNT_OF_TWEETS_TO_BE_FETCHED = 10000
        top_songs_count = 10

        # Twitter API Results
        results = defaultdict(list)
        final_results = defaultdict(list)

        # API Results Combined
        collected_tweets = defaultdict(list)

        # Only The Status info from Collected Tweets
        parsed_tweets2 = defaultdict()
        parsed_tweets3 = defaultdict()

        # Result Holders
        text_array = []
        index_array = []
        top_songs_array = []

        # -----------------------------------------------------#
        # Get Data from Twitter API---------------------------#
        # -----------------------------------------------------#

        for i in range(0, MAX_ATTEMPTS):

            if (COUNT_OF_TWEETS_TO_BE_FETCHED < len(final_results)):
                break  # we got 500 tweets... !!

            # ----------------------------------------------------------------#
            # STEP 1: Query Twitter
            # STEP 2: Save the returned tweets
            # STEP 3: Get the next max_id
            # ----------------------------------------------------------------#

            # STEP 1: Query Twitter
            if (0 == i):
                # Query twitter for data.
                final_results = twitter.search(
                    q="#NowPlaying open.spotify ♫",
                    count='100',
                    geocode=geocode_val)
            else:
                # After the first call we should have max_id from result of previous call.
                # Pass it in query.
                results = twitter.search(
                    q="#NowPlaying open.spotify ♫",
                    count='100',
                    include_entities='true',
                    max_id=next_max_id,
                    geocode=geocode_val)

                collected_tweets['statuses'].extend(results['statuses'])

                # STEP 3: Get the next max_id
            try:
                # Parse the data returned to get max_id to be passed in consequent call.
                if (0 == i):
                    next_results_url_params = final_results['search_metadata']['next_results']
                else:
                    next_results_url_params = results['search_metadata']['next_results']
                next_max_id = next_results_url_params.split('max_id=')[1].split('&')[0]
            except:
                # No more next pages
                break

        # Result Parameters ---------------------------------------------------------#
        # Tweet Number, number of tweets collected
        tnum = len(collected_tweets['statuses'])

        # Only The Status info from Collected Tweets
        parsed_tweets = (collected_tweets['statuses'])
        # +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++


        # -----------------------------------------------------#
        # Regex and Orginize 'text' field---------------------#
        # -----------------------------------------------------#
        for t in range(0, tnum):
            aa = parsed_tweets[t]
            parsed_tweets2[t] = dict((k, aa[k]) for k in ('created_at', 'id'))
            text = aa['text']
            text2 = re.findall(r'(?<=#NowPlaying )([^"]*)(?= ♫)', text)
            if text2 == []:
                text7 = []
            else:
                text3 = text2[0]
                text4 = text3.replace(" by ", " - ")
                text5 = text4.replace(" de ", " - ")
                text6 = text5.replace(" von ", " - ")
                text7 = text6.replace(" di ", " - ")
            parsed_tweets2[t]['text'] = text7
            text_array.append(text7)

            # Check if "url" is empty if not; Collect only spotify url
            collected_urls = aa['entities']['urls']
            if collected_urls == []:
                link = []
            else:
                link = collected_urls[0]['expanded_url']
            parsed_tweets2[t]['url'] = link
            # ----------------------------------------------------------------#

            # Check if "user" is empty if not; Collect only lang and location
            collected_user = aa['user']
            if collected_user == []:
                user = []
            else:
                lang = collected_user['lang']
                location = collected_user['location']
            parsed_tweets2[t]['lang'] = lang
            parsed_tweets2[t]['location'] = location
            # ----------------------------------------------------------------#

        # Assign occurance count for each entity with a new key on a dict object
        for t in range(0, tnum):
            search_text = text_array[t]
            t_count = text_array.count(search_text)
            parsed_tweets2[t]['count'] = t_count

        # -----------------------------------------------------#
        # Sort Dict of Dict using occurrence count ------------#
        # -----------------------------------------------------#

        sorted_tweets = sorted(parsed_tweets2, key=lambda x: parsed_tweets2[x]['count'], reverse=True)

        for i in range(0, tnum):
            if (top_songs_count > len(top_songs_array)):
                top_song = parsed_tweets2[sorted_tweets[i]]['text']
                if top_song not in top_songs_array:
                    top_songs_array.append(parsed_tweets2[sorted_tweets[i]]['text'])
                    index_array.append(sorted_tweets[i])

        # -----------------------------------------------------#
        # Collect tweets using indexes ------------------------#
        # -----------------------------------------------------#
        for j in range(0, len(index_array)):
            bb = parsed_tweets2[index_array[j]]
            parsed_tweets3[j] = dict((k, bb[k]) for k in parsed_tweets2[0].keys())

        return parsed_tweets3
