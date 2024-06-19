import lib.twitter_importer as twitter_importer
from lib.tweet_splitter import split_authors, split_json, split_locations
from lib.data_exporter import DataExporter
from lib.sentiment_analyzer import analyze_tweet_sentiments, analyze_tweet_keywords
import json
import sys


############################################################
#   Tweet-Pulling Functions
############################################################

def pull_topic_tweets(in_topic, token):
    """
    Pulls 100 tweets for the given topic.

    @param in_topic: String; the topic that we want to pull tweets for.
    @param token: (If given) the next page of results to pull tweets from.
    @return next_token: The next pagination token for the same topic.
    """

    ############################################################
    #   Fetching Tweets
    ############################################################
    topic = in_topic
    query_params = {'query': (topic + ' -is:retweet lang:en'),
                    'tweet.fields': 'created_at,geo',
                    'max_results': 100,
                    'expansions': 'author_id,geo.place_id'}

    ############################################################
    #   Pagination Control Here
    ############################################################
    if (token != None):
        query_params['next_token'] = token

    print("INFO: Starting tweet import.")
    response = twitter_importer.fetch_tweets(query_params)

    # Should allow us to get the next page of tweets...
    next_token = response['meta']['next_token']

    ############################################################
    #   Splitting Tweets
    ############################################################
    tweet_list = split_json(response)
    author_list = split_authors(response)
    location_list = split_locations(response)

    ############################################################
    #   Filtering Tweets Down to Remove Duplicates
    ############################################################
    data_uploader = DataExporter()
    tweet_list = data_uploader.check_existing_tweets(tweet_list)

    ############################################################
    #   Iterating Through Tweets & Exporting to DB
    ############################################################
    deleted_authors = []
    deleted_locations = []
    counter = 1
    for tweet in tweet_list:
        ##############################
        # Adding User to Table
        ##############################
        user_id = 0
        remove_author = None
        for author in author_list:
            if (tweet['author_id'] == author['id']):
                user_id = data_uploader.addUser(author)
                remove_author = author
                break

        if (remove_author is not None):  # Remove author from list to shorten iteration time
            author_list.remove(remove_author)
            deleted_authors.append(remove_author)
        else:  # However, multiple tweets from the same author can be pulled; so go here if the author is not found.
            for author in deleted_authors:
                if (tweet['author_id'] == author['id']):
                    user_id = data_uploader.addUser(author)
                    break

        ##############################
        # Add Location to Table
        ##############################
        location_id = 0
        remove_location = None
        if tweet['location'] is not None:  # If the tweet is geo-tagged

            # Search for matching location in the location list.
            for place in location_list:
                if (tweet['location'] == place['id']):
                    location_id = data_uploader.addLocation(place)
                    remove_location = place
                    break

            # Remove the location to speed up iteration
            if (remove_location is not None):
                location_list.remove(remove_location)
                deleted_locations.append(remove_location)
            else:  # Find the location in the deleted list if all else fails
                for place in location_list:
                    if (tweet['location'] == place['id']):
                        location_id = data_uploader.addLocation(place)
                        break

        ##############################
        # Adding Tweet to Table
        ##############################
        data_uploader.add_tweet(topic, tweet, user_id, location_id)

        ##############################
        # Finding Hashtags & Adding
        ##############################
        data_uploader.add_tweet_tags(tweet)

        print("INFO: " + str(counter) + " out of " +
              str(len(tweet_list)) + " tweets pulled.")
        counter += 1

    print("INFO: Tweet import finished.")

    ############################################################
    #   Cognitive Analysis & Upload to DB
    ############################################################
    print("INFO: Starting Azure analysis.")
    tweet_sentiments = analyze_tweet_sentiments(tweet_list)
    tweet_keywords = analyze_tweet_keywords(tweet_list)

    for tweet in tweet_sentiments:
        data_uploader.add_tweet_sentiment_info(tweet)

    counter = 1
    for tweet in tweet_keywords:
        data_uploader.add_tweet_keywords(tweet, topic)
        print("INFO: " + str(counter) + " out of " +
              str(len(tweet_list)) + " tweets complete.")
        counter += 1

    print("INFO: Analysis finished.")
    print("=================================================")
    return next_token


def pull_topic(in_topic, num_desired):
    """
    Pulls in all of the desired tweets for a given topic.

    @param in_topic: String; the topic we want to pull tweets for.
    @param num_desired: The number of tweets we want for that given topic
    """

    print("\n=================================================")
    print("\tFetching Tweets for : " + in_topic)
    print("=================================================")
    tweet_count = 0
    next_token = None
    while (tweet_count < num_desired):
        next_token = pull_topic_tweets(in_topic, next_token)
        tweet_count += 100
    print("\n=================================================")
    print("\tDone Fetching Tweets for : " + in_topic)
    print("=================================================")


############################################################
#   Main
############################################################
def main():
    data_uploader = DataExporter()

    first_topic = input("Enter in your first topic: ")
    pull_topic(first_topic, 500)
    second_topic = input("Enter in your second topic: ")
    pull_topic(second_topic, 500)
    third_topic = input("Enter in your third topic: ")
    pull_topic(third_topic, 500)

    print("\n\n Done!")


main()
