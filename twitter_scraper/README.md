# Twitter Scrapper

A project written in Python to get old tweets, it bypass some limitations of Twitter Official API.

## Details

This code is based on this one:

>https://github.com/Jefferson-Henrique/GetOldTweets-python

It has been rewrote to work properly on Python3. There's work still in progress (use of more modern libraries, changes in style to conform to PEP8, etc)

Twitter Official API has the bother limitation of time constraints: you can't get older tweets than a week. Some tools provide access to older tweets but in the most of them you have to spend some money before.
This code imitates how Twitter Search through a browser works: when you enter on Twitter a scroll loader starts, if you scroll down you get more and more tweets, all through calls to a JSON provider.

## Gender Pay Gap DataHack

We gathered thousands of tweets from December 2017 until June 2018 and you can find them in [pay_gap_data](./pay_gap_data), there is one JSON file for every month. You are very welcome to use this data or to do your own custom queries.

## Prerequisites

The code has been modified to be used with Python3 and it has not been tested in Python2.

Expected package dependencies are listed in the "requirements.txt" file for PIP, you need to run the following command to get dependencies:

```
    pip install -r requirements.txt
```

## Usage

To use this code you need to execute **search_tweets.py**
```
    python search_tweets.py [args]
```

with at least one of the following arguments:

 - --username: Username of a twitter account (without @)
 - --since: Start of datetime window (YYY-MM-DD)
 - --until: End of datetime window (YYYY-MM-DD)
 - --query: A query text to be matched
 - --near: A reference location area from where tweets were generated
 - --within: A distance radius from 'near' location
 - --language: Language of the tweets
 - --maxtweets: Maximun number of tweets to retrieve
 - --output: A filname to export the results

## What do you get?

The output is a json file with a name of your choosing or "output.json" as default. The file has all the tweets that match your query, each tweet with the following information:

  - id (str)
  - permalink (str)
  - username (str)
  - text (str)
  - date (date)
  - retweets (int)
  - favorites (int)
  - mentions (str)
  - hashtags (str)


## Examples of command-line usage
- Get help use
```
    python search_tweets.py -h
```
- Get tweets by username
```
    python search_tweets.py --username "barackobama" --maxtweets 1
```    
- Get tweets by query search
```
    python search_tweets.py --query "#paygap" --maxtweets 30
```    
- Get tweets by username and bound dates
```
    python search_tweets.py --username "barackobama" --since 2015-09-10 --until 2015-09-12 --maxtweets 1
```
