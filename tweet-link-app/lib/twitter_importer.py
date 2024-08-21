"""
twitter_importer is a module that simply contains the function used to fetch Tweets from the Twitter API.

@author Abigail Goodwin <abby.goodwin@outlook.com>

Copyright 2024, Abigail Goodwin, All rights reserved.
"""

import requests
import json
from pathlib import Path
import os

############################################################
#   Fetching Tweets
############################################################
def grab_bearer_token() -> str:
    """
    Attempts to grab the user's X API Bearer token from the project_config.json file.
    """
    current_path = os.path.dirname(os.path.realpath(__file__))
    config_file_path = Path(current_path).parent.parent.absolute()

    with open(f"{config_file_path}/project_config.json") as config_file:
        config_json = json.load(config_file)
        return config_json['twitter-api-info']['bearer-token']

def fetch_tweets(in_query_params):
    """
    Uses Twitter's API to request Tweets that match the given parameters.

    @param in_query_params: The query parameters to use.
    """
    search_url = "https://api.x.com/2/tweets/search/recent"
    auth_header = {
        'Authorization': f'Bearer {grab_bearer_token()}'
    }
    response = requests.get(search_url, headers=auth_header, params=in_query_params)
    response = json.loads(response.content.decode('utf-8'))
    return response
