"""
twitter_importer is a module that simply contains the function used to fetch Tweets from the Twitter API.

@author Abigail Goodwin <abby.goodwin@outlook.com>

Copyright 2022, Abigail Goodwin, All rights reserved.
"""

import requests
import json

# "Static" Attributes
bearer_token = 'PLACEHOLDER'
headers = {
    'Authorization': 'Bearer {}'.format(bearer_token),
    'User-Agent': 'PLACEHOLDER'
}

############################################################
#   Fetching Tweets
############################################################


def fetch_tweets(in_query_params):
    """
    Uses Twitter's API to request Tweets that match the given parameters.

    @param in_query_params: The query parameters to use.
    """
    search_url = "https://api.twitter.com/2/tweets/search/recent"
    response = requests.request(
        "GET", search_url, headers=headers, params=in_query_params)
    response = json.loads(response.content.decode('utf-8'))
    return response
