import urllib.request
import urllib.parse
import json
import re
import datetime
import sys
import http.cookiejar
import collections
from pyquery import PyQuery

Tweet = collections.namedtuple(
    "Tweet",
    "id permalink username text date formatted_date retweets favorites mentions hashtags geo urls author_id",
)


def _parse_tweet(html):
    """Tweet parser.
    Receives the html for a tweet and then identifies each portion with a corresponding argument.
    """
    tweetPQ = PyQuery(html)

    # descifering every part of the html
    username_tweet = (
        tweetPQ("span.username.username.u-dir.u-textTruncate").contents()[1].text
    )
    txt = re.sub(
        r"\s+",
        " ",
        tweetPQ("p.js-tweet-text").text().replace("# ", "#").replace("@ ", "@"),
    )
    retweets = int(
        tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount")
        .attr("data-tweet-stat-count")
        .replace(",", "")
    )
    favorites = int(
        tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount")
        .attr("data-tweet-stat-count")
        .replace(",", "")
    )
    date_sec = int(tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
    id_number = tweetPQ.attr("data-tweet-id")
    permalink = tweetPQ.attr("data-permalink-path")
    user_id = int(tweetPQ("a.js-user-profile-link").attr("data-user-id"))
    geo_span = tweetPQ("span.Tweet-geo")
    geo = geo_span.attr("title") if len(geo_span) else ""
    urls = []
    for link in tweetPQ("a"):
        try:
            urls.append((link.attrib["data-expanded-url"]))
        except KeyError:
            pass

    tweet = Tweet(
        id=id_number,
        permalink="https://twitter.com" + permalink,
        username=username_tweet,
        text=txt,
        date=datetime.datetime.fromtimestamp(date_sec),
        formatted_date=datetime.datetime.fromtimestamp(date_sec).strftime(
            "%a %b %d %X +0000 %Y"
        ),
        retweets=retweets,
        favorites=favorites,
        mentions=" ".join(re.compile("(@\\w*)").findall(txt)),
        hashtags=" ".join(re.compile("(#\\w*)").findall(txt)),
        geo=geo,
        urls=",".join(urls),
        author_id=user_id,
    )
    return tweet


def _get_tweet_batch_html(config, refresh_cursor, cookie_jar, proxy):
    """Scraper
    Identifies the tweets portion from the html json file
    """
    json = _get_json_response(config, refresh_cursor, cookie_jar, proxy)

    if len(json["items_html"].strip()) == 0:
        return
    refresh_cursor = json["min_position"]
    scraped_tweets = PyQuery(json["items_html"])
    # Remove incomplete tweets withheld by Twitter Guidelines
    scraped_tweets.remove("div.withheld-tweet")
    return scraped_tweets("div.js-stream-tweet")


def _get_json_response(config, refresh_cursor, cookie_jar, proxy):
    """JSON builder.
    Builds a URL from the arguments given by the user and gather a JSON file
    from that URL.
    """
    url = (
        "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&%smax_position=%s"
    )
    # creating the url
    url_get_data = ""
    if config.username is not None:
        url_get_data += " from:" + config.username

    if config.since is not None:
        url_get_data += " since:" + config.since

    if config.until is not None:
        url_get_data += " until:" + config.until

    if config.query is not None:
        url_get_data += " " + config.query

    if config.near is not None:
        url_get_data += "&near:" + config.near + " within:" + config.within

    if config.language is not None:
        url_lang = "l=" + config.language + "&"
    else:
        url_lang = ""
    url = url % (urllib.parse.quote(url_get_data), url_lang, refresh_cursor)

    headers = [
        ("Host", "twitter.com"),
        ("User-Agent", "Mozilla/5.0 (Windows NT 4.1; Win64; x64)"),
        ("Accept", "application/json, text/javascript, */*; q=0.01"),
        ("Accept-Language", "en_UK,en-US;q=0.7,en;q=0.3"),
        ("X-Requested-With", "XMLHttpRequest"),
        ("Referer", url),
        ("Connection", "keep-alive"),
    ]

    if proxy:
        opener = urllib.request.build_opener(
            urllib.request.ProxyHandler({"http": proxy, "https": proxy}),
            urllib.request.HTTPCookieProcessor(cookie_jar),
        )
    else:
        opener = urllib.request.build_opener(
            urllib.request.HTTPCookieProcessor(cookie_jar)
        )
    opener.addheaders = headers

    try:
        response = opener.open(url)
        json_response = response.read()
    except:
        print(
            "Twitter weird response. Try to see on browser: "
            "https://twitter.com/search?q={}&src=typd".format(
                urllib.parse.quote(url_get_data)
            ),
            file=sys.stderr,
            flush=True,
        )

        raise

    data_json = json.loads(json_response.decode("utf-8"))

    return data_json


def get_tweets(config, proxy=None):
    """Tweets generator.
    It receives the arguments parsed in 'search_tweets' and passes them to
    the rest of the functions to obtain the tweets.
    returns: generator
    """
    # variable that mimics the scroll in the web
    refresh_cursor = ""
    # automatic handling of HTTP cookies
    cookie_jar = http.cookiejar.CookieJar()
    # counter for number of tweets received
    parsed_tweets = 0

    while True:
        tweets_html = _get_tweet_batch_html(config, refresh_cursor, cookie_jar, proxy)

        if tweets_html is None or len(tweets_html) == 0:
            break

        for tweet_html in tweets_html:

            tweet = _parse_tweet(tweet_html)
            yield tweet
            parsed_tweets += 1

            if config.maxtweets and parsed_tweets >= config.maxtweets:
                return
