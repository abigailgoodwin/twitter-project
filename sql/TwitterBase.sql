PRAGMA foreign_keys;

DROP TABLE IF EXISTS TweetKeyPhrases;
DROP TABLE IF EXISTS TweetHashtags;
DROP TABLE IF EXISTS TweetSentiment;
DROP TABLE IF EXISTS TweetConfidence;
DROP TABLE IF EXISTS Tweets;
DROP TABLE IF EXISTS Users;
DROP TABLE IF EXISTS ConfidenceTypes;
DROP TABLE IF EXISTS Hashtags;
DROP TABLE IF EXISTS Locations;
DROP TABLE IF EXISTS KeyPhrases;
DROP TABLE IF EXISTS Sentiments;

CREATE TABLE Users
(
    UserID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    AuthorID bigint NOT NULL,
    UserHandle nvarchar(255) NOT NULL,
    UserName nvarchar(255) NOT NULL
);

CREATE TABLE Locations
(
    LocationID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    LocationCode nvarchar(255) NOT NULL,
    LocationName nvarchar(255) NOT NULL
);

CREATE TABLE Tweets
(
    TweetID bigint PRIMARY KEY NOT NULL,
    TweetAuthorID int NOT NULL,
    TweetDate datetime NOT NULL,
    LocationID int DEFAULT NULL,
    TweetBody nvarchar(255) NOT NULL,
    TweetJSON nvarchar(255) NOT NULL,
    TweetTopic nvarchar(255) NOT NULL,
    FOREIGN KEY (TweetAuthorID) REFERENCES Users(UserID),
    FOREIGN KEY (LocationID) REFERENCES Locations(LocationID)
);

CREATE TABLE ConfidenceTypes
(
    ConfidenceTypeID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    ConfidenceLabel nvarchar(255) NOT NULL
);

CREATE TABLE Hashtags
(
    HashtagID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    HashtagText nvarchar(255) NOT NULL
);

CREATE TABLE KeyPhrases
(
    KeyPhraseID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    KeyPhraseText nvarchar(255) NOT NULL
);

CREATE TABLE Sentiments
(
    SentimentID int IDENTITY(1,1) PRIMARY KEY NOT NULL,
    SentimentName nvarchar(255) NOT NULL
);

CREATE TABLE TweetSentiment
(
    TweetID bigint NOT NULL,
    SentimentID int NOT NULL,
    FOREIGN KEY (TweetID) REFERENCES Tweets(TweetID),
    FOREIGN KEY (SentimentID) REFERENCES Sentiments(SentimentID),
    PRIMARY KEY (TweetID, SentimentID)
);

CREATE TABLE TweetConfidence
(
    TweetID bigint NOT NULL,
    ConfidenceTypeID int NOT NULL,
    ConfidenceScore DECIMAL(3, 2) NOT NULL,
    FOREIGN KEY (TweetID) REFERENCES Tweets(TweetID),
    FOREIGN KEY (ConfidenceTypeID) REFERENCES ConfidenceTypes(ConfidenceTypeID),
    PRIMARY KEY (TweetID, ConfidenceTypeID)
);

CREATE TABLE TweetKeyPhrases
(
    TweetID bigint NOT NULL,
    KeyPhraseID int NOT NULL,
    FOREIGN KEY (TweetID) REFERENCES Tweets(TweetID),
    FOREIGN KEY (KeyPhraseID) REFERENCES KeyPhrases(KeyPhraseID),
    PRIMARY KEY (TweetID, KeyPhraseID)
);

CREATE TABLE TweetHashtags
(
    TweetID bigint NOT NULL,
    HashtagID int NOT NULL,
    FOREIGN KEY (TweetID) REFERENCES Tweets(TweetID),
    FOREIGN KEY (HashtagID) REFERENCES Hashtags(HashtagID),
    PRIMARY KEY (TweetID, HashtagID)
);

INSERT INTO ConfidenceTypes (ConfidenceTypeID, ConfidenceLabel)
VALUES
    (1, 'positive'),
    (2, 'neutral'),
    (3, 'negative');

INSERT INTO Sentiments (SentimentID, SentimentName)
VALUES
    (1, 'positive'),
    (2, 'neutral'),
    (3, 'mixed'),
    (4, 'negative');
