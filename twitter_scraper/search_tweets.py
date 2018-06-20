import argparse, datetime
from tweet_manager import get_tweets
import json


def main():
    """Gathers the user's arguments and pass them to the tweet_manager to search for and build the tweets """

    try:

        tweet_parser = argparse.ArgumentParser(prog="tweet_scrapper")
        tweet_parser.add_argument(
            "--username", type=str, help="Username of a twitter account (without @)"
        )
        tweet_parser.add_argument(
            "--since", help="start of datetime window, format YYYY-MM-DD"
        )
        tweet_parser.add_argument(
            "--until", help="end of datetime window, format YYYY-MM-DD"
        )
        tweet_parser.add_argument(
            "--query", type=str, help="A query text to be matched"
        )
        tweet_parser.add_argument(
            "--near",
            type=str,
            help="A reference location area from where tweets were generated",
        )
        tweet_parser.add_argument(
            "--within",
            type=str,
            default="15mi",
            help='A distance radius from "near" location. Default: "15mi"',
        )
        tweet_parser.add_argument(
            "--language", default="en", help="Language of the tweets(default: english)"
        )
        tweet_parser.add_argument(
            "--maxtweets",
            type=int,
            default=0,
            help="The maximun number of tweets to retrieve",
        )
        tweet_parser.add_argument(
            "--output",
            type=str,
            default="output.json",
            help='A filename to export the results (default:"output.json")',
        )
        config = tweet_parser.parse_args()

        print("\nSearching...")

        all_tweets = []

        for tweet in get_tweets(config):
            all_tweets.append(
                {
                    "username": tweet.username,
                    "id": tweet.id,
                    "permalink": tweet.permalink,
                    "timestamp": tweet.date.strftime("%Y-%m-%d %H:%M"),
                    "tweet": tweet.text,
                    "retweets": tweet.retweets,
                    "favorites": tweet.favorites,
                    "mentions": tweet.mentions,
                    "hashtags": tweet.hashtags,
                }
            )

        with open(config.output, "w") as f:
            f.write(
                json.dumps(all_tweets, ensure_ascii=False, sort_keys=True, indent=4)
                + "\n"
            )

    except ValueError:
        msg = "Not a valid type"
        raise argparse.ArgumentTypeError(msg)
    finally:
        print("\nDone. Output file generated: '{}'".format(config.output))


if __name__ == "__main__":
    main()
