# Overview: Tweet Analysis Project
Author: Abigail Goodwin <abby.goodwin@outlook.com>
## 50,000 Foot View

In short, this project is a Python application that prompts users for three topics. The application then uses Twitter's API to grab 1,000 Tweets related to each topic and stores them in a local database. At this point, these Tweets are pushed through Microsoft's Cognitive Services to determine their overall sentiment (positive, neutral, negative) and any significant keywords. Once this data is aggregated, a PowerBI dashboard imports the database's rows to create a visualization of the data retrieved.

## Topics Demonstrated

This project demonstrates my knowledge of relational database design and implementation. Along the way, a few other concepts are also demonstrated:

- Usage of Twitter's API to retrieve "Tweets" on user-selected topics.
- Usage of Microsoft's Cognitive Services to analyze the sentiment of a piece of text.
- Usage of Microsoft's Cognitive Services to determine keywords in a piece of text.
- Usage of PowerBI to visualize the overall sentiment for the Tweets retrieved on a specific topic.
- Usage of PowerBI to create word maps for each topic's most common keywords.

# How Do I Run the Project?

## Required Tools/Packages

To run this application, it is assumed that you have:

- Python 3.8 or Greater
- pip 20.0 or Greater (typically installed with the above)
- Access to a Twitter API endpoint
- Access to an Azure Services endpoint

## Step 1: Configure the Project

The first step to running this application is to install its required dependencies.

1. Open a terminal in this project's root folder (`twitter-project/`).
2. Run the following command: `pip install -r requirements.txt`. This will install this project's dependencies.
3. Ensure that your API Bearer tokens have been added to the project's `project_config.json` file.

## Step 2: Run the App

At this point, you should have the prerequisite packages to run this app.

1. Open a terminal in the `tweet-link-app/` directory.
2. Run the following command: `python3 ./TweetScanApp.py`. This should start up the application for you.

## Step 3: Using the App
1. When started, the app will automatically prompt you for your first topic.
2. Provide your first topic by typing the topic in the terminal and then pressing ENTER.
3. Repeat steps 1-2 for your other two topics.
4. It may take some time after entering your topics for the app to finish its analysis - this is normal.

> Copyright 2024, Abigail Goodwin, All rights reserved.
