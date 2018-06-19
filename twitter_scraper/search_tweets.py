import argparse, datetime
from tweet_manager import TweetManager
import json

def main():

    try:

        tweet_parser = argparse.ArgumentParser(prog='tweet_scrapper')
        tweet_parser.add_argument('--username',
                                  type=str,
                                  help='Username of a twitter account (without @)')
        tweet_parser.add_argument('--since',
                                  help='start of datetime window, format YYYY-MM-DD')
        tweet_parser.add_argument('--until',
                                  help='end of datetime window, format YYYY-MM-DD')
        tweet_parser.add_argument('--query',
                                  type=str,
                                  help='A query text to be matched')
        tweet_parser.add_argument('--near',
                                  type=str,
                                  help='A reference location area from where tweets were generated')
        tweet_parser.add_argument('--within',
                                  type=str,
                                  default="15mi",
                                  help='A distance radius from "near" location. Default: "15mi"')
        tweet_parser.add_argument('--language',
                                  default="en"
                                  help='Language of the tweets(default: english)')
        tweet_parser.add_argument('--maxtweets',
                                  type=int,
                                  default=0,
                                  help='The maximun number of tweets to retrieve')
        tweet_parser.add_argument('--output',
                                  type=str,
                                  default="output.json",
                                  help='A filename to export the results (default:"output.json")')
        args = tweet_parser.parse_args()

        print('\nSearching...')

        all_tweets = []

        def receive_buffer(tweets):
            for t in tweets:
                all_tweets.append({"username": t.username,
                                   "id": t.id,
                                   "permalink": t.permalink,
                                   "timestamp": t.date.strftime("%Y-%m-%d %H:%M"),
                                   "tweet": t.text,
                                   "retweets": t.retweets,
                                   "favorites": t.favorites,
                                   "mentions": t.mentions,
                                   "hashtags": t.hashtags,
                                   }
                                   )

        TweetManager.get_tweets(args, receive_buffer)
        with open(args.output, 'w') as f:
            f.write(json.dumps(all_tweets, ensure_ascii=False, sort_keys=True, indent=4)+'\n')

    except ValueError:
        msg = "Not a valid type"
        raise argparse.ArgumentTypeError(msg)
    finally:
        print('\nDone. Output file generated: "%s".' % args.output)

if __name__ == '__main__':
    main()
