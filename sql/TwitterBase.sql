CREATE SCHEMA TwitterBase;

DROP TABLE IF EXISTS TwitterBase.TweetKeyPhrases, TwitterBase.TweetHashtags, TwitterBase.TweetSentiment, TwitterBase.TweetConfidence, TwitterBase.Tweets;
DROP TABLE IF EXISTS TwitterBase.Users, TwitterBase.ConfidenceTypes, TwitterBase.Hashtags, TwitterBase.Locations, TwitterBase.KeyPhrases, TwitterBase.Sentiments;

CREATE TABLE TwitterBase.Users
(
    UserID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    AuthorID bigint NOT NULL,
    UserHandle nvarchar(255) NOT NULL,
    UserName nvarchar(255) NOT NULL
)

CREATE TABLE TwitterBase.Locations
(
    LocationID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    LocationCode nvarchar(255) NOT NULL,
    LocationName nvarchar(255) NOT NULL
)

CREATE TABLE TwitterBase.Tweets
(
    TweetID bigint PRIMARY KEY NOT NULL,
    TweetAuthorID int NOT NULL, 
    TweetDate datetime NOT NULL,
    LocationID int DEFAULT NULL, 
    TweetBody nvarchar(255) NOT NULL,
    TweetJSON nvarchar(255) NOT NULL,
    TweetTopic nvarchar(255) NOT NULL
)

CREATE TABLE TwitterBase.ConfidenceTypes
(
    ConfidenceTypeID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    ConfidenceLabel nvarchar(255) NOT NULL
)

CREATE TABLE TwitterBase.Hashtags
(
    HashtagID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    HashtagText nvarchar(255) NOT NULL
)

CREATE TABLE TwitterBase.KeyPhrases
(
    KeyPhraseID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    KeyPhraseText nvarchar(255) NOT NULL
)

CREATE TABLE TwitterBase.Sentiments
(
    SentimentID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    SentimentName nvarchar(255) NOT NULL
)

CREATE TABLE TwitterBase.TweetSentiment
(
    TweetID bigint NOT NULL,
    SentimentID int NOT NULL
    CONSTRAINT PK_TweetSentiment PRIMARY KEY
	(
		TweetID,
		SentimentID
	)
)

CREATE TABLE TwitterBase.TweetConfidence
(
    TweetID bigint NOT NULL,
    ConfidenceTypeID int NOT NULL,
    ConfidenceScore DECIMAL(3, 2) NOT NULL
    CONSTRAINT PK_TweetConfidence PRIMARY KEY
	(
		TweetID,
        ConfidenceTypeID
	)
)

CREATE TABLE TwitterBase.TweetKeyPhrases
(
    TweetID bigint NOT NULL, 
    KeyPhraseID int NOT NULL
    CONSTRAINT PK_TweetKeyPhrases PRIMARY KEY
	(
		TweetID,
		KeyPhraseID
	)
)

CREATE TABLE TwitterBase.TweetHashtags
(
    TweetID bigint NOT NULL, 
    HashtagID int NOT NULL 
    CONSTRAINT PK_TweetHashtags PRIMARY KEY
	(
		TweetID,
		HashtagID
	)
)

ALTER TABLE TwitterBase.Tweets
ADD CONSTRAINT FK_Tweets1 FOREIGN KEY (TweetAuthorID)
	REFERENCES TwitterBase.Users (UserID)

ALTER TABLE TwitterBase.Tweets
ADD CONSTRAINT FK_Tweets2 FOREIGN KEY (LocationID)
    REFERENCES TwitterBase.Locations (LocationID)

ALTER TABLE TwitterBase.TweetSentiment
ADD CONSTRAINT FK_TweetSentiment1 FOREIGN KEY (TweetID)
	REFERENCES TwitterBase.Tweets (TweetID)

ALTER TABLE TwitterBase.TweetSentiment
ADD CONSTRAINT FK_TweetSentiment2 FOREIGN KEY (SentimentID)
	REFERENCES TwitterBase.Sentiments (SentimentID)

ALTER TABLE TwitterBase.TweetConfidence
ADD CONSTRAINT FK_TweetConfidence1 FOREIGN KEY (TweetID)
    REFERENCES TwitterBase.Tweets (TweetID)

ALTER TABLE TwitterBase.TweetConfidence
ADD CONSTRAINT FK_TweetConfidence3 FOREIGN KEY (ConfidenceTypeID)
    REFERENCES TwitterBase.ConfidenceTypes (ConfidenceTypeID)

ALTER TABLE TwitterBase.TweetKeyPhrases
ADD CONSTRAINT FK_TweetKeyPhrases1 FOREIGN KEY (TweetID)
    REFERENCES TwitterBase.Tweets (TweetID)

ALTER TABLE TwitterBase.TweetKeyPhrases
ADD CONSTRAINT FK_TweetKeyPhrases2 FOREIGN KEY (KeyPhraseID)
    REFERENCES TwitterBase.KeyPhrases (KeyPhraseID)

ALTER TABLE TwitterBase.TweetHashtags
ADD CONSTRAINT FK_TweetHashtags1 FOREIGN KEY (TweetID)
    REFERENCES TwitterBase.Tweets (TweetID)

ALTER TABLE TwitterBase.TweetHashtags
ADD CONSTRAINT FK_TweetHashtags2 FOREIGN KEY (HashtagID)
    REFERENCES TwitterBase.Hashtags (HashtagID)


SET IDENTITY_INSERT TwitterBase.ConfidenceTypes ON
INSERT INTO TwitterBase.ConfidenceTypes (ConfidenceTypeID, ConfidenceLabel)
VALUES
    (1, 'positive'),
    (2, 'neutral'),
    (3, 'negative')

SET IDENTITY_INSERT TwitterBase.ConfidenceTypes OFF

SET IDENTITY_INSERT TwitterBase.Sentiments ON
INSERT INTO TwitterBase.Sentiments (SentimentID, SentimentName)
VALUES
    (1, 'positive'),
    (2, 'neutral'),
    (3, 'mixed'),
    (4, 'negative')

SET IDENTITY_INSERT TwitterBase.Sentiments OFF

