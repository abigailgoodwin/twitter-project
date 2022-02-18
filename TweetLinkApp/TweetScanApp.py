import lib.TwitterImporter as TwitterImporter
from lib.TweetSplitter import splitAuthors, splitJson, splitLocations
from lib.DataExporter import DataExporter
from lib.SentimentAnalyzer import analyzeTweetSentiments, analyzeTweetKeywords
import json
import pyodbc
import sys


############################################################
#   Tweet-Pulling Functions
############################################################
    
'''
    pullTopicTweets: Pulls 100 tweets for the given topic.
    @param in_topic: String; the topic that we want to pull tweets for.
    @param token: (If given) the next page of results to pull tweets from.
    @return nextToken: The next pagination token for the same topic.
'''
def pullTopicTweets(in_topic, token):
    ############################################################
    #   Fetching Tweets
    ############################################################
    topic = in_topic
    query_params = {'query': (topic + ' -is:retweet lang:en'),
                    'tweet.fields' : 'created_at,geo',
                    'max_results': 100,
                    'expansions': 'author_id,geo.place_id'}
    
    ############################################################
    #   Pagination Control Here
    ############################################################
    if (token != None):
        query_params['next_token'] = token
    
    print("INFO: Starting tweet import.")
    response = TwitterImporter.fetchTweets(query_params)
    
    nextToken = response['meta']['next_token'] # Should allow us to get the next page of tweets...
    
    ############################################################
    #   Splitting Tweets
    ############################################################
    tweetList = splitJson(response)
    authorList = splitAuthors(response)
    locationList = splitLocations(response)
    
    ############################################################
    #   Filtering Tweets Down to Remove Duplicates
    ############################################################
    dataUploader = DataExporter()
    tweetList = dataUploader.checkExistingTweets(tweetList)
    
    ############################################################
    #   Iterating Through Tweets & Exporting to DB
    ############################################################
    deletedAuthors = []
    deletedLocations = []
    counter = 1
    for tweet in tweetList:
        ##############################
        # Adding User to Table
        ##############################
        userID = 0
        removeAuthor = None
        for author in authorList:
            if(tweet['author_id'] == author['id']):
                userID = dataUploader.addUser(author)
                removeAuthor = author
                break
        
        if (removeAuthor is not None):  # Remove author from list to shorten iteration time
            authorList.remove(removeAuthor)
            deletedAuthors.append(removeAuthor)
        else: # However, multiple tweets from the same author can be pulled; so go here if the author is not found.
            for author in deletedAuthors:
                if(tweet['author_id'] == author['id']):
                    userID = dataUploader.addUser(author)
                    break
        
        ##############################
        # Add Location to Table
        ##############################
        locationID = 0
        removeLocation = None
        if tweet['location'] is not None: # If the tweet is geo-tagged
            
            # Search for matching location in the location list.
            for place in locationList:
                if(tweet['location'] == place['id']):
                    locationID = dataUploader.addLocation(place)
                    removeLocation = place
                    break
                
            # Remove the location to speed up iteration
            if (removeLocation is not None):
                locationList.remove(removeLocation)
                deletedLocations.append(removeLocation)
            else: # Find the location in the deleted list if all else fails
                for place in locationList:
                    if(tweet['location'] == place['id']):
                        locationID = dataUploader.addLocation(place)
                        break
    
        ##############################
        # Adding Tweet to Table
        ##############################
        dataUploader.addTweet(topic, tweet, userID, locationID)
    
        ##############################
        # Finding Hashtags & Adding
        ##############################
        dataUploader.addTweetTags(tweet)
        
        print("INFO: " + str(counter) + " out of " + str(len(tweetList)) + " tweets pulled.")
        counter += 1
    
    print("INFO: Tweet import finished.")
        
    ############################################################
    #   Cognitive Analysis & Upload to DB
    ############################################################
    print("INFO: Starting Azure analysis.")
    tweetSentiments = analyzeTweetSentiments(tweetList)
    tweetKeywords = analyzeTweetKeywords(tweetList)
    
    for tweet in tweetSentiments:
        dataUploader.addTweetSentimentInfo(tweet)
        
    counter = 1
    for tweet in tweetKeywords:
        dataUploader.addTweetKeywords(tweet, topic)
        print("INFO: " + str(counter) + " out of " + str(len(tweetList)) + " tweets complete.")
        counter += 1
        
    print("INFO: Analysis finished.")
    print("=================================================")
    return nextToken
    
'''
    pullTopic: Pulls in all of the desired tweets for a given topic.
    @param in_topic: String; the topic we want to pull tweets for.
    @param numDesired: The number of tweets we want for that given topic
    
'''
def pullTopic(in_topic, numDesired):
    print("\n=================================================")
    print("\tFetching Tweets for : " + in_topic)
    print("=================================================")
    tweetCount = 0
    nextToken = None
    while (tweetCount < numDesired):
        nextToken = pullTopicTweets(in_topic,nextToken)
        tweetCount += 100
    print("\n=================================================")
    print("\tDone Fetching Tweets for : " + in_topic)
    print("=================================================")
        
        
############################################################
#   Main
############################################################
def main():
    firstTopic = input("Enter in your first topic: ")
    pullTopic(firstTopic, 500)
    secondTopic = input("Enter in your second topic: ")
    pullTopic(secondTopic, 500)
    thirdTopic = input("Enter in your third topic: ")
    pullTopic(thirdTopic, 500)
    
    print("\n\n Done!")

main()
