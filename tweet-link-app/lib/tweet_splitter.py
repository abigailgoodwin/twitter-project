import json
"""
    tweet_splitter is in charge of taking raw JSON and converting it into a list of separated tweets.
    The "list of separated tweets" will be a list of dictionaries.
    
    @author Abby Goodwin <abigailgoodwin@mail.weber.edu>
    @date 12/02/2021
"""


def split_json(raw_json):
    """
    split_json will take in raw JSON and convert it into a list of dictionaries.

    @param raw_json: A super long JSON string. Contains 10 or more tweets.
    @return List of dictionaries; tweets split into individual dictionaries.
    """
    tweet_list = []

    # Converts each tweet into a dictionary and then adds it to the list
    for tweet in raw_json['data']:
        location = None

        # If the tweet comes with location data.
        if 'geo' in tweet:
            location = tweet['geo']
            location = location['place_id']

        tweet_list.append(
            {'id': tweet['id'],
             'author_id': tweet['author_id'],
             'created_at': get_date_time(tweet),
             'location': location,  # Searched for Geo data; if it doesn't exist, then 'None'
             'text': tweet['text']}
        )

    return tweet_list


def split_authors(raw_json):
    """
    split_authors: Splits the authors from the raw_json into their own list.
    @param raw_json: A super long JSON string. Contains 10 or more tweets.
    @return author_list: List of dictionaries; authors split into individual dictionaries.
    """

    author_list = []

    for user in raw_json['includes']['users']:
        author_list.append(
            {'id': user['id'],
             'name': user['name'],
             'username': user['username']})

    return author_list


def split_locations(raw_json):
    """
    Splits the locations from the raw_json into their own list.

    @param raw_json: A super long JSON string. Contains 10 or more tweets.
    @return location_list: List of dictionaries; locations split into individual dictionaries.
    """
    location_list = []

    if (len((raw_json['includes'])) > 2):
        for place in raw_json['includes']['places']:
            location_list.append(
                {'id': place['id'],
                 'full_name': place['full_name']})

    return location_list


def get_date_time(tweet):
    """
    Gets the data and time associated with the given tweet.

    @param tweet: The incoming tweet.
    """
    raw_string = tweet['created_at']

    # Step 1: Separate Time from Date
    date_end = raw_string.find("T")
    date = raw_string[:date_end]
    time = raw_string[date_end+1:(len(raw_string)-5)]
    datetime = date + ' ' + time

    return datetime


def collect_hashtags(tweet):
    """
    Creates a list of the hashtags associated with the given Tweet.

    @param tweet: The given Tweet.
    """

    hashtag_list = []  # List of hashtags per tweet.
    tweet_text = tweet['text']

    tag_start = 0
    while (tag_start < len(tweet_text) and tag_start >= 0):
        tag_start = tweet_text.find("#", tag_start)

        if (tag_start >= 0):  # If the tag exists, find its end
            for char_index in range(tag_start+1, len(tweet_text)):
                current_char = tweet_text[char_index]
                if (current_char in [' ', '#', ',', '!', '.', '?', '\n', '\"', ':', ';']):
                    tag_end = char_index
                    break

                tag_end = len(tweet_text)

            hashtag = tweet_text[tag_start:tag_end]
            hashtag_list.append(hashtag)

            tag_start = tag_end

    return hashtag_list
