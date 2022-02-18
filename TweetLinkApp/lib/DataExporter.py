'''
DataExporter: the file in charge of opening a connection to the database and querying the database.
@author Abigail Goodwin <abby.goodwin@outlook.com>
'''

import pyodbc
from TweetSplitter import collectHashtags

'''
    DataExporter: Responsible for sending data to the database.
    
    Decided that I'd probably need an object for this to maintain the connection.
'''
class DataExporter:
    ############################################################
    #   Class Attributes (DB Info)
    ############################################################
    # Absolutely NOT good coding practice. Need to obfuscate this data. Never connect to a database so openly like this.
    #   Simply a placeholder.
    server = ''
    database = ''
    username = ''
    password = '' 
    connection = None
    cursor = None

    ############################################################
    #   Constructor/Destructor
    ############################################################
    '''
        __init__: Constructor. Opens up a connection to the database when the object is called (and used).
    '''
    def __init__(self):
        self.connection = pyodbc.connect('DRIVER={SQL Server Native Client 11.0};SERVER=' +
                            self.server + ';DATABASE=' + self.database +
                            ';UID=' + self.username + ';PWD=' + self.password)
        self.cursor = self.connection.cursor()
        print("INFO: Connection opened to " + self.server + ".")
        
    '''
        __del__: Destructor. Closes the connection to the database when the object goes out of scope.
    '''
    def __del__(self):
      self.connection.close()
      print("INFO: Connection to " + self.server + " closed.")
      
    ############################################################
    #   Class Methods
    ############################################################
    '''
    addUser: Adds the user that wrote the given tweet to the Users table.
    @param tweet: A tweet
    @return userID: the primary key for the newly created author.
    '''
    def addUser(self, author):
        sql_query = '''
            DECLARE @created_user_id int
            EXEC TwitterBase.InsertAuthor ?,?,?,@userID = @created_user_ID OUTPUT
            SELECT @created_user_ID AS [userID]
        '''
        args = (int(author['id']), author['username'], author['name'])
        self.cursor.execute(sql_query, args)
        rows = self.cursor.fetchall()
        created_user_ID = rows[0][0]
        self.cursor.commit()
        
        return created_user_ID
    
    '''
        addLocation: Adds a locaton to the Locations table.
        @param tweet: A tweet.
        @return created_location_id: Primary key for the newly created Locations row.
    '''
    def addLocation(self, place):
        sql_query = '''
            DECLARE @created_location_id INT
            EXEC TwitterBase.InsertLocation ?,?, @LocationID = @created_location_id OUTPUT
            SELECT @created_location_id AS [LocationID]
        '''
        args = (place['id'], place['full_name'])
        self.cursor.execute(sql_query, args)
        rows = self.cursor.fetchall()
        created_location_id = rows[0][0]
        self.cursor.commit()
        
        return created_location_id

    '''
        addTweet: Adds a tweet to the Tweets table.
        @param tweet: The tweet that we are adding.
        @param tweetAuthorID: the UserID for the Author (PK in Users table)
        @param locationID: the LocationID for the Location (PK in Locations table)
        @return void
        
        <Query Info>
        tweetID: The tweet's ID (created by Twitter, not us)
        authorID: The author's ID (should have been created before, passed in)
        locationID: The location ID (should have been created, passed in as param)  
    '''
    def addTweet(self, topic, tweet, tweetAuthorID, locationID):
        sql_query = '''
            DECLARE @newDateTime datetime
            SET @newDateTime = CONVERT(DATETIME, ?)
            EXEC TwitterBase.InsertTweet ?,?,?,@newDateTime,?,?,?
        '''
        args = (tweet['created_at'], int(tweet['id']), tweetAuthorID, locationID, tweet['text'], str(tweet), topic)
        self.cursor.execute(sql_query, args)
        self.cursor.commit()

    '''
        ***DEPRECATED***
        addHashtags: Adds all the hashtags for a given tweet to the Hashtags table.
        @param tweet: The tweet we're getting hashtags from.
        @return hashTagIDList: list of hashtag IDS connected to the given tweet.
    '''
    def addHashtags(self, tweet):
        hashTagList = collectHashtags(tweet)
        hashTagIDList = []
        
        for hashtag in hashTagList:
            sql_query = '''
            DECLARE @created_tag_ID int
            EXEC TwitterBase.InsertHashtags ?, @hashtagID = @created_tag_ID OUTPUT
            SELECT @created_tag_ID AS [tagID]
            '''
            args = (hashtag)
            self.cursor.execute(sql_query, args)
            rows = self.cursor.fetchall()
            created_tag_ID = rows[0][0]
            hashTagIDList.append(created_tag_ID)
            self.cursor.commit()
        
        return hashTagIDList

    '''
        addTweetTags: Adds to the junction table (TweetHashtags) a tweet and its corresponding hashtags.
        @param tweet: The tweet that we're adding to the junction table.
        @param tagList: The list of Tweet Hashtag IDs.
        @return void
    '''
    def addTweetTags(self, tweet):
        tagList = collectHashtags(tweet)
        for tag in tagList:
            sql_query = '''
            EXEC TwitterBase.InsertHashtags ?,?
            '''
            args = (int(tweet['id']), tag)
            self.cursor.execute(sql_query, args)
            self.cursor.commit()
                 
                 
    '''
        addTweetSentimentInfo: Adds the corresponding tweet's sentiment analysis info to the DB.
        @param tweetInfo: Python dictionary that contains the tweet's id, sentiment, confidence scores, and keywords.
        @return void
    '''
    def addTweetSentimentInfo(self, tweetInfo):
            sql_query = '''
            EXEC TwitterBase.InsertSentimentInfo ?,?,?,?,?
            '''
            args = (int(tweetInfo['id']), tweetInfo['overall_sentiment'], tweetInfo['confidence_scores']['positive'], tweetInfo['confidence_scores']['neutral'], tweetInfo['confidence_scores']['negative'])
            self.cursor.execute(sql_query, args)
            self.cursor.commit()
      
    '''
        addTweetKeywords: Adds the corresponding tweet's keywords, as given by Cognitive Services, to the DB.
        @param tweetInfo: Python dictionary that contains the tweet's id, sentiment, confidence scores, and keywords.
        @return void
    '''
    def addTweetKeywords(self, tweetInfo, topic):
        keywordList = tweetInfo['key_phrases']
        tweetID = tweetInfo['id']
        
        for phrase in keywordList:
            if(topic not in phrase and topic.lower() not in phrase and topic.upper() not in phrase): # We don't want the topic as a keyword.                              
                # Step 1: Insert Key Phrase Into DB
                sql_query = '''
                DECLARE @created_keyphrase_ID int
                EXEC TwitterBase.InsertKeyPhrase ?,?, @KeyPhraseID = @created_keyphrase_ID OUTPUT
                SELECT @created_keyphrase_ID
                '''
                args = (int(tweetID), phrase)
                self.cursor.execute(sql_query, args)
                rows = self.cursor.fetchall()
                created_phrase_ID = rows[0][0]
                # Step 2: Insert Into Junction Table
                sql_query = '''EXEC TwitterBase.InsertTweetKeyPhrases ?,?'''
                args = (int(tweetID), int(created_phrase_ID))
                self.cursor.execute(sql_query, args)
                self.cursor.commit()
     
    '''
        checkExistingTweets: Checks if there are duplicate tweets already in the database, and returns a filtered list of those that aren't.
        @param tweetList: The list of tweets before filtering.
        @return list; List of tweets, not including the tweets already in the database.
    '''       
    def checkExistingTweets(self, tweetList):
        newTweetList = []
        
        for tweet in tweetList:
            sql_query = '''
            SELECT COUNT(*) FROM TwitterBase.Tweets AS T WHERE T.TweetID = ?
            '''
            args = (int(tweet['id']))
            self.cursor.execute(sql_query, args)
            rows = self.cursor.fetchall()
            numExisting = int(rows[0][0])
            
            if (numExisting == 0):
                newTweetList.append(tweet)
        
        return newTweetList
        
      
    
