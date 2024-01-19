CREATE OR ALTER PROCEDURE TwitterBase.InsertAuthor
(
    @authorID bigint,
    @UserHandle nvarchar(255),
    @UserName nvarchar(255),
    @userID int OUTPUT
)
AS
BEGIN
    SET NOCOUNT ON
    IF (SELECT COUNT(*) FROM TwitterBase.Users AS U WHERE U.AuthorID = @authorID) = 0
        BEGIN
            INSERT INTO TwitterBase.Users (AuthorID, UserHandle, UserName)
            VALUES
                (@authorID, @UserHandle, @UserName)
        END

    SELECT @userID = UserID FROM TwitterBase.Users WHERE AuthorID = @authorID
    SET NOCOUNT OFF
END

GO
CREATE OR ALTER PROCEDURE TwitterBase.InsertLocation
(
    @locationCode nvarchar(255),
    @locationName nvarchar(255),
    @locationID int OUTPUT
)
AS
BEGIN
    SET NOCOUNT ON
    
    IF (SELECT COUNT(*) FROM TwitterBase.Locations AS L WHERE L.LocationCode = @locationCode) = 0
    BEGIN
        INSERT INTO TwitterBase.Locations (LocationCode, LocationName)
        VALUES
            (@locationCode, @locationName)
    END

    SELECT @locationID = LocationID FROM TwitterBase.Locations WHERE LocationCode = @locationCode

    SET NOCOUNT OFF
END

GO
CREATE OR ALTER PROCEDURE TwitterBase.InsertTweet
(
    @TweetID bigint,
    @TweetAuthorID int,
    @LocationID nvarchar(255),
    @TweetDate datetime,
    @TweetBody nvarchar(255),
    @TweetJSON nvarchar(255),
    @TweetTopic nvarchar(255)
)
AS
BEGIN
    SET NOCOUNT ON

    IF (SELECT COUNT(*) FROM TwitterBase.Tweets AS T WHERE T.TweetID = @TweetID) = 0
    BEGIN
        INSERT INTO TwitterBase.Tweets (TweetID, TweetAuthorID, LocationID, TweetDate, TweetBody, TweetJSON, TweetTopic)
        VALUES
            (@TweetID, @TweetAuthorID, (CASE WHEN @LocationID != 0 THEN @LocationID ELSE NULL END), @TweetDate, @TweetBody, @TweetJSON, @TweetTopic)
    END

    SET NOCOUNT OFF 
END

GO
CREATE OR ALTER PROCEDURE TwitterBase.InsertHashtags
(
    @TweetID bigint,
    @hashtagText nvarchar(255)
)
AS
BEGIN
    SET NOCOUNT ON

    IF (SELECT COUNT(*) FROM TwitterBase.Hashtags AS H WHERE H.HashtagText = @hashtagText) = 0
    BEGIN
        INSERT INTO TwitterBase.Hashtags (HashtagText)
        VALUES
            (@hashtagText)
    END

    DECLARE @HashtagID INT
    SET @HashtagID = (SELECT HashtagID FROM TwitterBase.Hashtags AS H WHERE H.HashtagText = @hashtagText)

    IF (SELECT COUNT(*) FROM TwitterBase.TweetHashtags AS TH WHERE TH.TweetID = @TweetID AND TH.HashtagID = @HashtagID) = 0
    BEGIN
        INSERT INTO TwitterBase.TweetHashtags (TweetID, HashtagID)
        VALUES
            (@TweetID, @HashtagID)
    END    

    SET NOCOUNT OFF
END

GO
CREATE OR ALTER PROCEDURE TwitterBase.InsertSentimentInfo
(
    @TweetID bigint,
    @OverallSentiment nvarchar(255),
    @CScore_Positive decimal(3,2),
    @CScore_Neutral decimal(3,2),
    @CScore_Negative decimal(3,2)
)
AS
BEGIN
    SET NOCOUNT ON

    IF (SELECT COUNT(*) FROM TwitterBase.TweetSentiment AS TS WHERE TS.TweetID = @TweetID) = 0
    BEGIN
        DECLARE @TweetSentimentID INT
        SET @TweetSentimentID = CASE
                                WHEN @OverallSentiment = 'positive' THEN 1
                                WHEN @OverallSentiment = 'neutral' THEN 2
                                WHEN @OverallSentiment = 'mixed' THEN 3
                                WHEN @OverallSentiment = 'negative' THEN 4
                                END;

        INSERT INTO TwitterBase.TweetSentiment (TweetID, SentimentID)
        VALUES
            (@TweetID, @TweetSentimentID)
    
    END
    IF (SELECT COUNT(*) FROM TwitterBase.TweetConfidence AS TC WHERE TC.TweetID = @TweetID) < 3
    BEGIN

        INSERT INTO TwitterBase.TweetConfidence (TweetID, ConfidenceTypeID, ConfidenceScore)
        VALUES
            (@TweetID, 1, @CScore_Positive),
            (@TweetID, 2, @CScore_Neutral),
            (@TweetID, 3, @CScore_Negative)
        
    END

    SET NOCOUNT OFF
END

GO
CREATE OR ALTER PROCEDURE TwitterBase.InsertKeyPhrase
(
    @TweetID bigint,
    @TweetKeyword nvarchar(255),
    @KeyPhraseID int OUTPUT
)
AS
BEGIN
    SET NOCOUNT ON
    
    IF (SELECT COUNT(*) FROM TwitterBase.KeyPhrases WHERE KeyPhraseText = @TweetKeyword) = 0
    BEGIN
        
        INSERT INTO TwitterBase.KeyPhrases (KeyPhraseText)
        VALUES
            (@TweetKeyword)

    END

    SELECT @KeyPhraseID = KeyPhraseID FROM TwitterBase.KeyPhrases AS KP WHERE KP.KeyPhraseText = @TweetKeyword

    SET NOCOUNT OFF
END

GO
CREATE OR ALTER PROCEDURE TwitterBase.InsertTweetKeyPhrases
(
    @TweetID bigint,
    @KeyPhraseID int
)
AS
BEGIN
    SET NOCOUNT ON

    IF (SELECT COUNT(*) FROM TwitterBase.TweetKeyPhrases WHERE TweetID = @TweetID AND KeyPhraseID = @KeyPhraseID) = 0
    BEGIN

        INSERT INTO TwitterBase.TweetKeyPhrases (TweetID, KeyPhraseID)
        VALUES
            (@TweetID, @KeyPhraseID)
    END

    SET NOCOUNT OFF
END