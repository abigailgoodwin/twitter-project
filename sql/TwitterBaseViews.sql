WITH DistinctTweets
AS
(
    SELECT DISTINCT
        T.TweetID
    FROM
        TwitterBase.Tweets AS T
)
SELECT
    COUNT(*)
FROM
    DistinctTweets


GO
CREATE OR ALTER VIEW TwitterBase.TweetUserView
AS
    SELECT DISTINCT
        T.TweetTopic,
        T.TweetID,
        U.UserHandle,
        T.TweetDate,
        L.LocationName,
        T.TweetBody,
        T.TweetJSON

    FROM
        TwitterBase.Tweets AS T
        INNER JOIN TwitterBase.Users AS U
            ON T.TweetAuthorID = U.UserID
        LEFT JOIN TwitterBase.Locations AS L
            ON T.LocationID = L.LocationID

GO
CREATE OR ALTER VIEW TwitterBase.TweetTagView
AS
    SELECT
        T.TweetID,
        H.HashtagText

    FROM
        TwitterBase.Tweets AS T
        INNER JOIN TwitterBase.TweetHashtags AS TH
            ON T.TweetID = TH.TweetID
        INNER JOIN TwitterBase.Hashtags AS H
            ON TH.HashtagID = H.HashtagID

GO
CREATE OR ALTER VIEW TwitterBase.TweetSentimentView
AS
    WITH TweetConTable
    AS
    (
        SELECT
            TS.TweetID,
            S.SentimentName,
            CT.ConfidenceLabel,
            TC.ConfidenceScore
        FROM
            TwitterBase.TweetSentiment AS TS
            INNER JOIN TwitterBase.Sentiments AS S
                ON TS.SentimentID = S.SentimentID
            INNER JOIN TwitterBase.TweetConfidence AS TC
                ON TS.TweetID = TC.TweetID
            INNER JOIN TwitterBase.ConfidenceTypes AS CT
                ON TC.ConfidenceTypeID = CT.ConfidenceTypeID
    )
    SELECT
        PVT.TweetID,
        PVT.SentimentName AS [OverallSentiment],
        PVT.[positive],
        PVT.[neutral],
        PVT.[negative]

    FROM
        TweetConTable AS TC
        PIVOT
        (
            MAX(TC.ConfidenceScore)
            FOR TC.ConfidenceLabel IN ([positive], [neutral], [negative])
        ) AS PVT

GO
CREATE OR ALTER VIEW TwitterBase.TweetPhraseView
AS
    SELECT
        TKP.TweetID,
        KP.KeyPhraseText

    FROM
        TwitterBase.TweetKeyPhrases AS TKP
        INNER JOIN TwitterBase.KeyPhrases AS KP
            ON TKP.KeyPhraseID = KP.KeyPhraseID

GO
CREATE OR ALTER VIEW TwitterBase.NegativeTweets
AS
    SELECT
        T.TweetID,
        T.TweetTopic

    FROM
        TwitterBase.TweetSentiment AS TS
        INNER JOIN TwitterBase.Sentiments AS S
            ON TS.SentimentID = S.SentimentID
        INNER JOIN TwitterBase.Tweets AS T
            ON TS.TweetID = T.TweetID

    WHERE
        S.SentimentName = 'negative'

GO
CREATE OR ALTER VIEW TwitterBase.AbortionTweets
AS
    SELECT
        *
    
    FROM
        TwitterBase.Tweets

    WHERE
        TweetTopic = 'Abortion'

GO
CREATE OR ALTER VIEW TwitterBase.GunControlTweets
AS
    SELECT
        *
    
    FROM
        TwitterBase.Tweets

    WHERE
        TweetTopic = 'Gun Control'

GO
CREATE OR ALTER VIEW TwitterBase.VaccineTweets
AS
    SELECT
        *
    
    FROM
        TwitterBase.Tweets

    WHERE
        TweetTopic = 'Vaccine'


GO
CREATE OR ALTER VIEW TwitterBase.PositiveTweets
AS
    SELECT
        T.TweetID,
        T.TweetTopic
    
    FROM
        TwitterBase.TweetSentiment AS TS
        INNER JOIN TwitterBase.Sentiments AS S
            ON TS.SentimentID = S.SentimentID
        INNER JOIN TwitterBase.Tweets AS T
            ON TS.TweetID = T.TweetID

    WHERE
        S.SentimentName = 'positive'


GO
CREATE OR ALTER VIEW TwitterBase.TweetDominantConfidenceScore
AS
    SELECT
        TC.TweetID,
        MAX(TC.ConfidenceScore) AS [Score]
    
    FROM
        TwitterBase.TweetConfidence AS TC
        INNER JOIN TwitterBase.TweetSentiment AS TS
            ON TC.TweetID = TS.TweetID
        INNER JOIN TwitterBase.ConfidenceTypes AS CT
            ON TC.ConfidenceTypeID = CT.ConfidenceTypeID

    GROUP BY
        TC.TweetID

GO
SELECT * FROM TwitterBase.TweetUserView ORDER BY TweetTopic, LocationName DESC
SELECT * FROM TwitterBase.TweetTagView
SELECT * FROM TwitterBase.TweetSentimentView
SELECT * FROM TwitterBase.TweetPhraseView