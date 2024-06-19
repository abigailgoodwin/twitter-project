"""
data_exporter: the file in charge of opening a connection to the database and querying the database.
@author Abigail Goodwin <abby.goodwin@outlook.com>
"""

import sqlite3
import os
from lib.tweet_splitter import collect_hashtags


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
        self.sql_path = os.path.realpath("sql/")

        # Create the TwitterBase SQLite DB in the SQL folder:
        self.connection = sqlite3.connect(
            os.path.join(self.sql_path, "TwitterBase.db"))

        # Store the cursor as a class member:
        self.cursor = self.connection.cursor()

        # Lastly, create the database's tables, views, and stored procedures:
        self.create_tables()

        print(
            f"INFO: Connection opened to SQLite Database at {self.sql_path}/db.")

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
                     "TwitterBaseViews.sql"]

        # Execute each script using SQLite:
        for sql_file_path in sql_files:
            # Open the SQL file and slurp its contents into a string:
            with open(os.path.join(self.sql_path, sql_file_path), "r") as sql_file:
                sql_script = sql_file.read()
                self.cursor.executescript(sql_script)
                self.connection.commit()

        print("INFO: SQLite Database Successfully Configured.")

    def verify_not_in_table(self, table_name, id_field_name, id) -> bool:
        """
        Verifies whether or not the given item is already in the database.

        @param table_name: The name of the Table to check.
        @param id_field_name: The name of the Primary Key's column.
        @param id: The unique identifier to check against.

        @return True if the item is not in the target table, or False otherwise.
        """
        sql_query = f"""
            SELECT COUNT(*) FROM {table_name} AS T WHERE T.{id_field_name} = {id}
        """
        rows = self.cursor.execute(sql_query)
        return True if rows.fetchall() is None else False

    def add_user(self, author):
        """
        Adds the user that wrote the given tweet to the Users table.

        @param tweet: A tweet
        @return userID: the primary key for the newly created author.
        """
        # First, verify that the author isn't already in the DB:
        not_in_table = self.verify_not_in_table(
            "Users", "AuthorID", author['id'])

        if not_in_table:
            # Below query insert the new author:
            sql_query = f"""
            INSERT INTO Users (AuthorID, UserHandle, UserName)
            VALUES
                ({author['id']}, {author['username']}, {author['name']})
            """
            self.cursor.execute(sql_query)
            self.connection.commit()

        # Grab the author's unique identifier (PK) from the DB:
        sql_query = f"""
        SELECT UserID FROM Users WHERE AuthorID = {author['id']}
        """
        rows = self.cursor.execute(sql_query)
        rows.fetchone()
        created_user_ID = rows[0]

        return created_user_ID

    def add_location(self, place):
        """
        Adds a locaton to the Locations table.

        @param tweet: A tweet.
        @return created_location_id: Primary key for the newly created Locations row.
        """
        not_in_table = self.verify_not_in_table(
            "Locations", "LocationCode", place['id'])

        if not_in_table:
            # Below query inserts the new location:
            sql_query = f"""
            INSERT INTO Locations (LocationCode, LocationName)
            VALUES
            ({place['id']}, {place['full_name']})
            """
            self.cursor.execute(sql_query)
            self.connection.commit()

        sql_query = f"""
            SELECT LocationID FROM Locations WHERE LocationCode = {place['id']}
        """
        rows = self.cursor.execute(sql_query)
        rows.fetchone()
        created_location_id = rows[0]

        return created_location_id

    def add_tweet(self, topic, tweet, tweet_author_id, location_id):
        """
        Adds a tweet to the Tweets table.

        @param tweet: The tweet that we are adding.
        @param tweet_author_id: the UserID for the Author (PK in Users table)
        @param location_id: the LocationID for the Location (PK in Locations table)
        @return void
        """
        # <Query Info>
        # tweet_id: The tweet's ID (created by Twitter, not us)
        # authorID: The author's ID (should have been created before, passed in)
        # location_id: The location ID (should have been created, passed in as param)

        # Verify that this exact Tweet isn't already in the DB:
        not_in_table = self.verify_not_in_table(
            "Tweets", "TweetID", tweet['id'])

        if not_in_table:
            # Convert the Tweet's creation date to a datetime object:
            sql_query = f"""
                CONVERT(DATETIME, {tweet['created_at']})
            """
            rows = self.cursor.execute(sql_query)
            rows.fetchone()
            date_time = rows[0]

            # Inser the Tweet into the table:
            sql_query = f"""
                INSERT INTO Tweets (TweetID, TweetAuthorID, LocationID, TweetDate, TweetBody, TweetJSON, TweetTopic)
                VALUES
                    ({tweet['id']}, {tweet_author_id}, {location_id if not None else "NULL"}, {date_time}, {tweet['text']}, {tweet}, {topic})
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
            not_in_table = self.verify_not_in_table(
                "Hashtags", "HashtagText", tag)

            # Insert the new tag:
            if not_in_table:
                sql_query = f"""
                    INSERT INTO Hashtags (HashtagText)
                    VALUES
                        ({tag})
                """
                self.cursor.execute(sql_query)
                self.connection.commit()

            # Query for the hashtag's ID from the hashtag table:
            sql_query = f"""
                SELECT HashtagID FROM Hashtags AS H WHERE H.HashtagText = {tag}
            """
            rows = self.cursor.execute(sql_query)
            rows.fetchone()
            hashtag_id = rows[0]

            # Check if this Tweet has already been mapped to this hashtag:
            sql_query = f"""
                SELECT COUNT(*) FROM TweetHashtags AS TH WHERE TH.TweetID = {tweet['id']} AND TH.HashtagID = {hashtag_id}
            """
            rows = self.cursor.execute(sql_query)
            rows.fetchall()

            # Only insert the new mapping if not already in the table:
            if rows is None:
                sql_query = f"""
                    INSERT INTO TweetHashtags (TweetID, HashtagID)
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

        # Verify that the Tweet has not already been mapped to a sentiment:
        not_in_table = self.verify_not_in_table(
            "TweetSentiment", "TweetID", tweet_info['id'])

        if not_in_table:
            # Convert the Tweet's sentiment to an integer:
            sentiments = {
                "positive": 1,
                "neutral": 2,
                "mixed": 3,
                "negative": 4
            }
            tweet_sentiment = sentiments[tweet_info['overall_sentiment']]

            # Map the Tweet to its overall sentiment:
            sql_query = f"""
                INSERT INTO TweetSentiment (TweetID, SentimentID)
                VALUES
                    ({tweet_info['id']}, {tweet_sentiment})
            """
            self.cursor.execute(sql_query)
            self.connection.commit()

        # Verify that the Tweet has not already been mapped to its Confidence values:
        sql_query = f"""
            SELECT COUNT(*) FROM TweetConfidence AS TC WHERE TC.TweetID = {tweet_info['id']}
        """
        rows = self.cursor.execute(sql_query)
        rows.fetchall()

        # There are three confidence values to track, so check if we have them:
        if len(rows) < 3:
            # Insert the Tweet's confidence scores for its assigned sentiment(s):
            sql_query = f"""
                INSERT INTO TweetConfidence (TweetID, ConfidenceTypeID, ConfidenceScore)
                VALUES
                    ({tweet_info['id']}, 1, {tweet_info['confidence_scores']['positive']}),
                    ({tweet_info['id']}, 2, {tweet_info['confidence_scores']['neutral']}),
                    ({tweet_info['id']}, 3, {tweet_info['confidence_scores']['negative']})
            """
            self.cursor.execute(sql_query)
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
            # We don't want the topic as a keyword. Have to filter for case here, as well.
            if (topic not in phrase and topic.lower() not in phrase and topic.upper() not in phrase):

                # Step 1: Insert Key Phrase Into DB if not already in the table:
                not_in_table = self.verify_not_in_table(
                    "KeyPhrases", "KeyPhraseText", phrase)

                if not_in_table:
                    sql_query = f"""
                    INSERT INTO KeyPhrases (KeyPhraseText)
                    VALUES
                        ({phrase})
                    """
                    self.cursor.execute(sql_query)
                    self.connection.commit()

                # Get the phrase's unique identifier in the KeyPhrases table:
                sql_query = f"""
                SELECT KeyPhraseID FROM KeyPhrases AS KP WHERE KP.KeyPhraseText = {phrase}
                """
                rows = self.cursor.execute(sql_query)
                rows.fetchone()
                created_phrase_ID = rows[0]

                # Lastly, check if the Tweet was already mapped to this phrase:
                sql_query = f"""
                    SELECT COUNT(*) FROM TweetKeyPhrases WHERE TweetID = {tweet_id} AND KeyPhraseID = {created_phrase_ID}
                """
                rows = self.cursor.execute(sql_query)
                rows.fetchall()

                if rows is None:
                    # Map the Tweet to the Key Phrase:
                    sql_query = f"""
                        INSERT INTO TweetKeyPhrases (TweetID, KeyPhraseID)
                        VALUES
                            ({tweet_id}, {created_phrase_ID})
                    """
                    self.cursor.execute(sql_query)
                    self.connection.commit()

    def check_existing_tweets(self, tweet_list):
        """
        Checks if there are duplicate tweets already in the database, and returns a filtered list of those that aren't.

        @param tweet_list: The list of tweets before filtering.
        @return list; List of tweets, not including the tweets already in the database.
        """
        new_tweet_list = []

        for tweet in tweet_list:
            sql_query = f"""
            SELECT COUNT(*) FROM Tweets AS T WHERE T.TweetID = {tweet['id']}
            """
            rows = self.cursor.execute(sql_query)
            rows.fetchall()
            num_existing = int(rows[0][0])

            if num_existing == 0:
                new_tweet_list.append(tweet)

        return new_tweet_list
