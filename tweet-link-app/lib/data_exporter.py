"""
data_exporter: the file in charge of opening a connection to the database and querying the database.
@author Abigail Goodwin <abby.goodwin@outlook.com>
"""

import sqlite3
import os
from tweet_splitter import collect_hashtags


class DataExporter:
    """
    Class responsible for creating the SQLite Database and populating its tables.
    """

    ############################################################
    #   Constructor/Destructor
    ############################################################

    def __init__(self):
        """
        Constructor. Opens up a connection to the database when the object is called (and used).
        """
        # Path to the project's sql folder:
        self.sql_path = os.path.realpath("../../sql/")

        # Create the TwitterBase SQLite DB in the SQL folder:
        self.connection = sqlite3.connect(
            os.path.join(self.sql_path, "TwitterBase.db"))

        # Store the cursor as a class member:
        self.cursor = self.connection.cursor()

        # Lastly, create the database's tables, views, and stored procedures:
        self.create_tables()

        print(
            f"INFO: Connection opened to SQLite Database at {self.sql_path}/TwitterBase.db.")

    def __del__(self):
        """
        Destructor. Closes the connection to the database when the object goes out of scope.
        """
        self.connection.close()
        print("INFO: Connection to SQLite Database closed.")

    ############################################################
    #   Class Methods
    ############################################################

    def create_tables(self) -> None:
        """
        Creates the database's schema, tables, views, and stored procedures.
        """
        # List of SQL files to execute:
        sql_files = ["TwitterBase.sql",
                     "TwitterBaseViews.sql", "TwitterProcs.sql"]

        # Execute each script using SQLite:
        for sql_file_path in sql_files:
            # Open the SQL file and slurp its contents into a string:
            with open(os.path.join(self.sql_path, sql_file_path), "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()

        print("INFO: SQLite Database Successfully Configured.")

    def add_user(self, author):
        """
        Adds the user that wrote the given tweet to the Users table.

        @param tweet: A tweet
        @return userID: the primary key for the newly created author.
        """
        # First, verify that the author isn't already in the DB:
        sql_query = f"""
            SELECT COUNT(*) FROM TwitterBase.Users AS U WHERE U.AuthorID = {author[id]}
        """
        rows = self.cursor.execute(sql_query)
        rows.fetchall()

        # Only inserts the author if they don't exist in the DB:
        if rows is None:
            # Below query insert the new author:
            sql_query = f"""
            INSERT INTO TwitterBase.Users (AuthorID, UserHandle, UserName)
            VALUES
                ({author['id']}, {author['username']}, {author['name']})
            """
            self.cursor.execute(sql_query)
            self.connection.commit()

        # Grab the author's unique identifier (PK) from the DB:
        sql_query = f"""
        SELECT UserID FROM TwitterBase.Users WHERE AuthorID = {author['id']}
        """
        rows = self.cursor.execute(sql_query)
        rows.fetchone()
        created_user_ID = rows[0][0]

        return created_user_ID

    def add_location(self, place):
        """
        Adds a locaton to the Locations table.

        @param tweet: A tweet.
        @return created_location_id: Primary key for the newly created Locations row.
        """
        sql_query = f"""
            SELECT COUNT(*) FROM TwitterBase.Locations AS L WHERE L.LocationCode = {place['id']}
        """
        rows = self.cursor.execute(sql_query)
        rows.fetchall()

        # Only insert the location if it doesn't already exist in the DB:
        if rows is None:
            # Below query inserts the new location:
            sql_query = f"""
            INSERT INTO TwitterBase.Locations (LocationCode, LocationName)
            VALUES
            ({place['id']}, {place['full_name']})
            """
            self.cursor.execute(sql_query)
            self.connection.commit()

        sql_query = f"""
            SELECT LocationID FROM TwitterBase.Locations WHERE LocationCode = {place['id']}
        """
        rows = self.cursor.execute(sql_query)
        rows.fetchone()
        created_location_id = rows[0][0]

        return created_location_id

    def add_tweet(self, topic, tweet, tweetAuthorID, locationID):
        """
        Adds a tweet to the Tweets table.

        @param tweet: The tweet that we are adding.
        @param tweetAuthorID: the UserID for the Author (PK in Users table)
        @param locationID: the LocationID for the Location (PK in Locations table)
        @return void
        """
        # <Query Info>
        # tweet_id: The tweet's ID (created by Twitter, not us)
        # authorID: The author's ID (should have been created before, passed in)
        # locationID: The location ID (should have been created, passed in as param)

        # Verify that this exact Tweet isn't already in the DB:
        sql_query = f"""
            SELECT COUNT(*) FROM TwitterBase.Tweets AS T Where T.TweetID = {tweet['id']}
        """
        rows = self.cursor.execute(sql_query)
        rows.fetchall()

        # Insert the new Tweet:
        if rows is None:

            # Convert the Tweet's creation date to a datetime object:
            sql_query = f"""
                CONVERT(DATETIME, {tweet['created_at']})
            """
            rows = self.cursor.execute(sql_query)
            rows.fetchone()
            date_time = rows[0][0]

            # Inser the Tweet into the table:
            sql_query = f"""
                INSERT INTO TwitterBase.Tweets (TweetID, TweetAuthorID, LocationID, TweetDate, TweetBody, TweetJSON, TweetTopic)
                VALUES
                    ({tweet['id']}, {tweetAuthorID}, {locationID if not None else "NULL"}, {date_time}, {tweet['text']}, {tweet}, {topic})
            """
            self.cursor.execute(sql_query)
            self.connection.commit()

    def add_tweet_tags(self, tweet):
        """
        Adds to the junction table (TweetHashtags) a tweet and its corresponding hashtags.

        @param tweet: The tweet that we're adding to the junction table.
        @param tag_list: The list of Tweet Hashtag IDs.
        @return void
        """
        tag_list = collect_hashtags(tweet)
        for tag in tag_list:
            # Verify that the Hashtag is not in the table already:
            sql_query = f"""
                SELECT COUNT(*) FROM TwitterBase.Hashtags AS H WHERE H.HashtagText = {tag}
            """
            rows = self.cursor.execute(sql_query)
            rows.fetchall()

            # Insert the new tag:
            if rows is None:
                sql_query = f"""
                    INSERT INTO TwitterBase.Hashtags (HashtagText)
                    VALUES
                        ({tag})
                """
                self.cursor.execute(sql_query)
                self.connection.commit()

            # Query for the hashtag's ID from the hashtag table:
            sql_query = f"""
                SELECT HashtagID FROM TwitterBase.Hashtags AS H WHERE H.HashtagText = {tag}
            """
            rows = self.cursor.execute(sql_query)
            rows.fetchone()
            hashtag_id = rows[0][0]

            # Check if this Tweet has already been mapped to this hashtag:
            sql_query = f"""
                SELECT COUNT(*) FROM TwitterBase.TweetHashtags AS TH WHERE TH.TweetID = {tweet['id']} AND TH.HashtagID = {hashtag_id}
            """
            rows = self.cursor.execute(sql_query)
            rows.fetchall()

            # Only insert the new mapping if not already in the table:
            if rows is None:
                sql_query = f"""
                    INSERT INTO TwitterBase.TweetHashtags (TweetID, HashtagID)
                    VALUES
                        ({tweet['id']}, {hashtag_id})
                """
                self.cursor.execute(sql_query)
                self.connection.commit()

    def add_tweet_sentiment_info(self, tweet_info):
        """
        Adds the corresponding tweet's sentiment analysis info to the DB.

        @param tweet_info: Python dictionary that contains the tweet's id, sentiment, confidence scores, and keywords.
        @return void
        """
        sql_query = """
        EXEC TwitterBase.InsertSentimentInfo ?,?,?,?,?
        """
        args = (int(tweet_info['id']), tweet_info['overall_sentiment'], tweet_info['confidence_scores']
                ['positive'], tweet_info['confidence_scores']['neutral'], tweet_info['confidence_scores']['negative'])
        self.cursor.execute(sql_query, args)
        self.connection.commit()

    def add_tweet_keywords(self, tweet_info, topic):
        """
        Adds the corresponding tweet's keywords, as given by Cognitive Services, to the DB.

        @param tweet_info: Python dictionary that contains the tweet's id, sentiment, confidence scores, and keywords.
        @return void
        """
        keyword_list = tweet_info['key_phrases']
        tweet_id = tweet_info['id']

        for phrase in keyword_list:
            # We don't want the topic as a keyword.
            if (topic not in phrase and topic.lower() not in phrase and topic.upper() not in phrase):
                # Step 1: Insert Key Phrase Into DB
                sql_query = """
                DECLARE @created_keyphrase_ID int
                EXEC TwitterBase.InsertKeyPhrase ?,?, @KeyPhraseID = @created_keyphrase_ID OUTPUT
                SELECT @created_keyphrase_ID
                """
                args = (int(tweet_id), phrase)
                self.cursor.execute(sql_query, args)
                rows = self.cursor.fetchall()
                created_phrase_ID = rows[0][0]
                # Step 2: Insert Into Junction Table
                sql_query = """EXEC TwitterBase.InsertTweetKeyPhrases ?,?"""
                args = (int(tweet_id), int(created_phrase_ID))
                self.cursor.execute(sql_query, args)
                self.connection.commit()

    def check_existing_tweets(self, tweet_list):
        """
        Checks if there are duplicate tweets already in the database, and returns a filtered list of those that aren't.

        @param tweet_list: The list of tweets before filtering.
        @return list; List of tweets, not including the tweets already in the database.
        """
        new_tweet_list = []

        for tweet in tweet_list:
            sql_query = """
            SELECT COUNT(*) FROM TwitterBase.Tweets AS T WHERE T.TweetID = ?
            """
            args = (int(tweet['id']))
            self.cursor.execute(sql_query, args)
            rows = self.cursor.fetchall()
            num_existing = int(rows[0][0])

            if (num_existing == 0):
                new_tweet_list.append(tweet)

        return new_tweet_list
