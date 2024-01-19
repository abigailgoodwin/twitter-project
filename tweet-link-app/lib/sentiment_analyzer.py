"""
sentiment_analyzer: the file in charge of analyzing tweet sentiment and keywords using Azure Cog Services.
@author Abigail Goodwin <abby.goodwin@outlook.com>
"""

from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

# "Static" Attributes
api_endpoint = 'https://example.cognitiveservices.azure.com/'
api_key = AzureKeyCredential('')  # Again, something you'd like to obfuscate.
api_call = TextAnalyticsClient(endpoint=api_endpoint, credential=api_key)

############################################################
#   Analyze Tweets
############################################################


def analyze_tweet(tweet):
    """
    Uses Cog Services to analyze the given tweet and return its sentiment, confidence, etc. DEPRECATED.

    @param tweet: The tweet being analyzed.
    @return tweetDetails: Python dictionary; the tweet's sentiment, confidence (positive, neutral, and negative), and key phrases.
    """
    api_document = []
    call_id = tweet['id']  # Just going to set this to the Tweet ID for now.
    api_document.append(
        {'id': str(call_id),
         'language': 'en',
         'text': tweet['text']}
    )

    raw_results = {}
    raw_results['sentiment'] = api_call.analyze_sentiment(
        api_document, show_opinion_mining=True)
    raw_results['key_words'] = api_call.extract_key_phrases(api_document)

    # Gives an atrocious output.... time to clean it up.
    sentiment_info = raw_results['sentiment'][0]
    keyword_info = raw_results['key_words'][0]

    clean_results = {}
    clean_results['id'] = call_id
    clean_results['overall_sentiment'] = sentiment_info['sentiment']
    clean_results['confidence_scores'] = sentiment_info['confidence_scores']
    clean_results['key_words'] = keyword_info['key_phrases']

    return clean_results


def batch(iterable, n=1):
    """
    Separates an iterable into batches for Azure processing purposes.

    @author Carl F. : https://stackoverflow.com/questions/8290397/how-to-split-an-iterable-in-constant-size-chunks
    """
    l = len(iterable)
    for ndx in range(0, l, n):
        yield iterable[ndx:min(ndx + n, l)]


def analyze_tweet_sentiments(tweet_list):
    """
    Analyzes a list of tweets using Azure's Cognitive Services for sentiment.

    @param tweet_list: A list of tweet text.
    @return tweet_sentiments: A Python dictionary of the tweet's overall sentiment and confidence levels (pos, neut, neg).
    """
    api_document = []

    # Step 1: Adding all of the tweets to the API call.
    for tweet in tweet_list:
        api_document.append(
            {
                'id': str(tweet['id']),
                'language': 'en',
                'text': tweet['text']
            }
        )

    # Step 2: Calling Azure in Batches
    raw_results = []
    for tweets in batch(api_document, 10):
        raw_results.append(api_call.analyze_sentiment(
            tweets, show_opinion_mining=True))

    # Step 3: Cleaning & Separating Data
    tweet_sentiments = []
    for group in raw_results:
        for tweet in group:
            tweet_info = {}
            tweet_info['id'] = tweet['id']
            tweet_info['overall_sentiment'] = tweet['sentiment']
            tweet_info['confidence_scores'] = tweet['confidence_scores']
            tweet_sentiments.append(tweet_info)

    return tweet_sentiments


def analyze_tweet_keywords(tweet_list):
    """
    Analyzes a list of tweets for their keywords.

    @param tweet_list: A list of tweet text.
    @return tweet_keywords: A Python dictionary of each tweet's keywords.
    """
    # Not sure if there's a guarantee that a tweet has keywords, so made another function.
    # @TODO: Filter down key phrases (opaquelist)
    api_document = []

    # Step 1: Adding all of the tweets to the API call.
    for tweet in tweet_list:
        api_document.append(
            {
                'id': str(tweet['id']),
                'language': 'en',
                'text': tweet['text']
            }
        )

    raw_results = []
    for tweets in batch(api_document, 10):
        raw_results.append(api_call.extract_key_phrases(tweets))

    tweet_keywords = []
    for group in raw_results:
        for tweet in group:
            tweet_info = {}
            tweet_info['id'] = tweet['id']
            tweet_info['key_phrases'] = tweet['key_phrases']
            tweet_keywords.append(tweet_info)

    return tweet_keywords
