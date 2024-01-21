WITH DistinctTweets
AS
(
    SELECT DISTINCT
        T.TweetID
    FROM
        Tweets AS T
)
SELECT
    COUNT(*)
FROM
    DistinctTweets


GO
CREATE OR ALTER VIEW TweetUserView
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
        Tweets AS T
        INNER JOIN Users AS U
            ON T.TweetAuthorID = U.UserID
        LEFT JOIN Locations AS L
            ON T.LocationID = L.LocationID

GO
CREATE OR ALTER VIEW TweetTagView
AS
    SELECT
        T.TweetID,
        H.HashtagText

    FROM
        Tweets AS T
        INNER JOIN TweetHashtags AS TH
            ON T.TweetID = TH.TweetID
        INNER JOIN Hashtags AS H
            ON TH.HashtagID = H.HashtagID

GO
CREATE OR ALTER VIEW TweetSentimentView
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
            TweetSentiment AS TS
            INNER JOIN Sentiments AS S
                ON TS.SentimentID = S.SentimentID
            INNER JOIN TweetConfidence AS TC
                ON TS.TweetID = TC.TweetID
            INNER JOIN ConfidenceTypes AS CT
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
CREATE OR ALTER VIEW TweetPhraseView
AS
    SELECT
        TKP.TweetID,
        KP.KeyPhraseText

    FROM
        TweetKeyPhrases AS TKP
        INNER JOIN KeyPhrases AS KP
            ON TKP.KeyPhraseID = KP.KeyPhraseID

GO
CREATE OR ALTER VIEW NegativeTweets
AS
    SELECT
        T.TweetID,
        T.TweetTopic

    FROM
        TweetSentiment AS TS
        INNER JOIN Sentiments AS S
            ON TS.SentimentID = S.SentimentID
        INNER JOIN Tweets AS T
            ON TS.TweetID = T.TweetID

    WHERE
        S.SentimentName = 'negative'

GO
CREATE OR ALTER VIEW AbortionTweets
AS
    SELECT
        *
    
    FROM
        Tweets

    WHERE
        TweetTopic = 'Abortion'

GO
CREATE OR ALTER VIEW GunControlTweets
AS
    SELECT
        *
    
    FROM
        Tweets

    WHERE
        TweetTopic = 'Gun Control'

GO
CREATE OR ALTER VIEW VaccineTweets
AS
    SELECT
        *
    
    FROM
        Tweets

    WHERE
        TweetTopic = 'Vaccine'


GO
CREATE OR ALTER VIEW PositiveTweets
AS
    SELECT
        T.TweetID,
        T.TweetTopic
    
    FROM
        TweetSentiment AS TS
        INNER JOIN Sentiments AS S
            ON TS.SentimentID = S.SentimentID
        INNER JOIN Tweets AS T
            ON TS.TweetID = T.TweetID

    WHERE
        S.SentimentName = 'positive'


GO
CREATE OR ALTER VIEW TweetDominantConfidenceScore
AS
    SELECT
        TC.TweetID,
        MAX(TC.ConfidenceScore) AS [Score]
    
    FROM
        TweetConfidence AS TC
        INNER JOIN TweetSentiment AS TS
            ON TC.TweetID = TS.TweetID
        INNER JOIN ConfidenceTypes AS CT
            ON TC.ConfidenceTypeID = CT.ConfidenceTypeID

    GROUP BY
        TC.TweetID

GO
SELECT * FROM TweetUserView ORDER BY TweetTopic, LocationName DESC
SELECT * FROM TweetTagView
SELECT * FROM TweetSentimentView
SELECT * FROM TweetPhraseView