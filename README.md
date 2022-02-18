Overview: Tweet Analysis Project
================================
This project, which I informally call the "Twitter Project," is a project that I did while learning some advanced database concepts. In short, it's goal is to:
* Allow the user to pick 3 topics.
* For each topic, 1,000 tweets are pulled down and stored into a local relational database.
* Each tweet is then run through Azure Cognitive Services to determine its overall sentiment and keywords.
* This sentiment analysis is then stored alongside its associated tweet in the database.
* At the end of the day, a PowerBI dashboard is generated that gives an overview of the results.
Naturally, there's a lot that went into it, so I'll be covering it in more detail below.

How Do I Run the Project?
=========================
At this point, I haven't formally applied any build tools. This means you're going to have to set up a virtual environment able to run this guy. You'll find the dependencies for this project in ```requirements.txt```.

> DISCLAIMER: The project will not run until after you've populated all of the database connection, Twitter API endpoint, and Azure Services endpoint information.

After you've done the above, you can run it by simply:
1. Navigate to the folder where ```TweetScanApp.py``` is.
2. Then, simply run from the terminal ```./TweetScanApp.py```.
3. The program will then take over and prompt you, via the terminal, for your topics.

PowerBI Notes
=============
As part of this project, I generated a PowerBI dashboard to visualize the data that I got back. This dashboard included:
* The top keywords across all three topics.
* The top 10 keywords for the negative and positive tweets for each category.
* The distribution of sentiments per each topic (i.e. what % of tweets were rated negative, positive, or mixed).
* And the distribution of confidence scores, provided by Azure, for each topic (on a scale of 0.00 to 1.00).

>**It's also worth noting that, at the time, I had already chosen my topics. The included PowerBI file and some SQL views reflect those topics.**

Other Notes
===========
* I've uploaded this to be a reference to my knowledge, not be a public application.
* For that reason, it's not in a "user-friendly" working state, as it has a) no build tools attached and b) all critical endpoints and connection info unimplemented.
* In the future, I may decide to turn this into a full-fledged application. But don't expect that any time soon!
