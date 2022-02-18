import json
'''
    TweetSplitter is in charge of taking raw JSON and converting it into a list of separated tweets.
    The "list of separated tweets" will be a list of dictionaries.
    
    @author Abby Goodwin <abigailgoodwin@mail.weber.edu>
    @date 12/02/2021
'''

'''
    splitJson will take in raw JSON and convert it into a list of dictionaries.
    
    @param raw_json: A super long JSON string. Contains 10 or more tweets.
    @return List of dictionaries; tweets split into individual dictionaries.
'''
def splitJson(raw_json):
    tweetList = []
    
    # Converts each tweet into a dictionary and then adds it to the list
    for tweet in raw_json['data']:
        location = None
        
        # If the tweet comes with location data.
        if 'geo' in tweet:
            location = tweet['geo']
            location = location['place_id']
            
        tweetList.append(
            {'id': tweet['id'],
             'author_id': tweet['author_id'],
             'created_at': getDateTime(tweet),
             'location': location, # Searched for Geo data; if it doesn't exist, then 'None'
             'text': tweet['text']}
            )
        
    return tweetList

'''
    splitAuthors: Splits the authors from the raw_json into their own list.
    @param raw_json: A super long JSON string. Contains 10 or more tweets.
    @return authorList: List of dictionaries; authors split into individual dictionaries.
'''
def splitAuthors(raw_json):
    authorList = []
    
    for user in raw_json['includes']['users']:
        authorList.append(
            {'id' : user['id'],
             'name' : user['name'],
             'username' : user['username']})
        
    return authorList

'''
    splitLocations: Splits the locations from the raw_json into their own list.
    @param raw_json: A super long JSON string. Contains 10 or more tweets.
    @return locationList: List of dictionaries; locations split into individual dictionaries.
'''
def splitLocations(raw_json):
    locationList = []
    
    if (len((raw_json['includes'])) > 2):
        for place in raw_json['includes']['places']:
            locationList.append(
                {'id' : place['id'],
                'full_name' : place['full_name']})
        
    return locationList
    

def getDateTime(tweet):
    rawString = tweet['created_at']
    
    # Step 1: Separate Time from Date
    dateEnd = rawString.find("T")
    date = rawString[:dateEnd]
    time = rawString[dateEnd+1:(len(rawString)-5)]
    datetime = date + ' ' + time
    
    return datetime
    

def collectHashtags(tweet):
    hashTagList = [] # List of hashtags per tweet.
    tweetText = tweet['text']
    
    tagStart = 0
    while (tagStart < len(tweetText) and tagStart >= 0):
        tagStart = tweetText.find("#", tagStart)
        
        if(tagStart >= 0): # If the tag exists, find its end
            for charIndex in range(tagStart+1, len(tweetText)):
                currentChar = tweetText[charIndex]
                if (currentChar in [' ', '#', ',', '!', '.','?', '\n', '\"', ':', ';']):
                    tagEnd = charIndex
                    break
                
                tagEnd = len(tweetText)
            
            hashtag = tweetText[tagStart:tagEnd]
            hashTagList.append(hashtag)
            
            tagStart = tagEnd
            
    return hashTagList