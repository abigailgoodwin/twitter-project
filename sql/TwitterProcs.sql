CREATE OR ALTER PROCEDURE InsertAuthor
(
    @authorID bigint,
    @UserHandle nvarchar(255),
    @UserName nvarchar(255),
    @userID int OUTPUT
)
AS
BEGIN
    SET NOCOUNT ON
    IF (SELECT COUNT(*) FROM Users AS U WHERE U.AuthorID = @authorID) = 0
        BEGIN
            INSERT INTO Users (AuthorID, UserHandle, UserName)
            VALUES
                (@authorID, @UserHandle, @UserName)
        END

    SELECT @userID = UserID FROM Users WHERE AuthorID = @authorID
    SET NOCOUNT OFF
END

GO
CREATE OR ALTER PROCEDURE InsertLocation
(
    @locationCode nvarchar(255),
    @locationName nvarchar(255),
    @locationID int OUTPUT
)
AS
BEGIN
    SET NOCOUNT ON
    
    IF (SELECT COUNT(*) FROM Locations AS L WHERE L.LocationCode = @locationCode) = 0
    BEGIN
        INSERT INTO Locations (LocationCode, LocationName)
        VALUES
            (@locationCode, @locationName)
    END

    SELECT @locationID = LocationID FROM Locations WHERE LocationCode = @locationCode

    SET NOCOUNT OFF
END

GO
CREATE OR ALTER PROCEDURE InsertTweet
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

    IF (SELECT COUNT(*) FROM Tweets AS T WHERE T.TweetID = @TweetID) = 0
    BEGIN
        INSERT INTO Tweets (TweetID, TweetAuthorID, LocationID, TweetDate, TweetBody, TweetJSON, TweetTopic)
        VALUES
            (@TweetID, @TweetAuthorID, (CASE WHEN @LocationID != 0 THEN @LocationID ELSE NULL END), @TweetDate, @TweetBody, @TweetJSON, @TweetTopic)
    END

    SET NOCOUNT OFF 
END

GO
CREATE OR ALTER PROCEDURE InsertHashtags
(
    @TweetID bigint,
    @hashtagText nvarchar(255)
)
AS
BEGIN
    SET NOCOUNT ON

    IF (SELECT COUNT(*) FROM Hashtags AS H WHERE H.HashtagText = @hashtagText) = 0
    BEGIN
        INSERT INTO Hashtags (HashtagText)
        VALUES
            (@hashtagText)
    END

    DECLARE @HashtagID INT
    SET @HashtagID = (SELECT HashtagID FROM Hashtags AS H WHERE H.HashtagText = @hashtagText)

    IF (SELECT COUNT(*) FROM TweetHashtags AS TH WHERE TH.TweetID = @TweetID AND TH.HashtagID = @HashtagID) = 0
    BEGIN
        INSERT INTO TweetHashtags (TweetID, HashtagID)
        VALUES
            (@TweetID, @HashtagID)
    END    

    SET NOCOUNT OFF
END

GO
CREATE OR ALTER PROCEDURE InsertSentimentInfo
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

    IF (SELECT COUNT(*) FROM TweetSentiment AS TS WHERE TS.TweetID = @TweetID) = 0
    BEGIN
        DECLARE @TweetSentimentID INT
        SET @TweetSentimentID = CASE
                                WHEN @OverallSentiment = 'positive' THEN 1
                                WHEN @OverallSentiment = 'neutral' THEN 2
                                WHEN @OverallSentiment = 'mixed' THEN 3
                                WHEN @OverallSentiment = 'negative' THEN 4
                                END;

        INSERT INTO TweetSentiment (TweetID, SentimentID)
        VALUES
            (@TweetID, @TweetSentimentID)
    
    END
    IF (SELECT COUNT(*) FROM TweetConfidence AS TC WHERE TC.TweetID = @TweetID) < 3
    BEGIN

        INSERT INTO TweetConfidence (TweetID, ConfidenceTypeID, ConfidenceScore)
        VALUES
            (@TweetID, 1, @CScore_Positive),
            (@TweetID, 2, @CScore_Neutral),
            (@TweetID, 3, @CScore_Negative)
        
    END

    SET NOCOUNT OFF
END

GO
CREATE OR ALTER PROCEDURE InsertKeyPhrase
(
    @TweetID bigint,
    @TweetKeyword nvarchar(255),
    @KeyPhraseID int OUTPUT
)
AS
BEGIN
    SET NOCOUNT ON
    
    IF (SELECT COUNT(*) FROM KeyPhrases WHERE KeyPhraseText = @TweetKeyword) = 0
    BEGIN
        
        INSERT INTO KeyPhrases (KeyPhraseText)
        VALUES
            (@TweetKeyword)

    END

    SELECT @KeyPhraseID = KeyPhraseID FROM KeyPhrases AS KP WHERE KP.KeyPhraseText = @TweetKeyword

    SET NOCOUNT OFF
END

GO
CREATE OR ALTER PROCEDURE InsertTweetKeyPhrases
(
    @TweetID bigint,
    @KeyPhraseID int
)
AS
BEGIN
    SET NOCOUNT ON

    IF (SELECT COUNT(*) FROM TweetKeyPhrases WHERE TweetID = @TweetID AND KeyPhraseID = @KeyPhraseID) = 0
    BEGIN

        INSERT INTO TweetKeyPhrases (TweetID, KeyPhraseID)
        VALUES
            (@TweetID, @KeyPhraseID)
    END

    SET NOCOUNT OFF
END