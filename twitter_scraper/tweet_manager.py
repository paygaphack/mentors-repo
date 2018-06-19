import urllib.request
import urllib.parse
import json
import re
import datetime
import sys
import http.cookiejar
import collections
from pyquery import PyQuery

Tweet = collections.namedtuple('Tweet', 'id permalink username text date formatted_date retweets favorites mentions hashtags geo urls author_id')

class TweetManager:

    def __init__(self):
        pass

    @staticmethod
    def get_tweets(args, receive_buffer=None, buffer_length=100, proxy=None):
        refresh_cursor = ''
        results = []
        results_aux = []
        # automatic handling of HTTP cookies
        cookie_jar = http.cookiejar.CookieJar()

        active = True

        while active:

            json = TweetManager.get_json_response(args, refresh_cursor, cookie_jar, proxy)

            if len(json['items_html'].strip()) == 0:
                break
            refresh_cursor = json['min_position']
            scraped_tweets = PyQuery(json['items_html'])
            # Remove incomplete tweets withheld by Twitter Guidelines
            scraped_tweets.remove('div.withheld-tweet')
            tweets = scraped_tweets('div.js-stream-tweet')



            if len(tweets) == 0:
                break

            for tweetHTML in tweets:
                tweetPQ = PyQuery(tweetHTML)

                # descifering every part of the html
                username_tweet = tweetPQ("span.username.username.u-dir.u-textTruncate").contents()[1].text
                txt = re.sub(
                    r"\s+", " ", tweetPQ("p.js-tweet-text").text().replace('# ', '#').replace('@ ', '@'))
                retweets = int(tweetPQ("span.ProfileTweet-action--retweet span.ProfileTweet-actionCount").attr(
                    "data-tweet-stat-count").replace(",", ""))
                favorites = int(tweetPQ("span.ProfileTweet-action--favorite span.ProfileTweet-actionCount").attr(
                    "data-tweet-stat-count").replace(",", ""))
                date_sec = int(
                    tweetPQ("small.time span.js-short-timestamp").attr("data-time"))
                id = tweetPQ.attr("data-tweet-id")
                permalink = tweetPQ.attr("data-permalink-path")
                user_id = int(
                    tweetPQ("a.js-user-profile-link").attr("data-user-id"))

                geo = ''
                geo_span = tweetPQ('span.Tweet-geo')
                if len(geo_span) > 0:
                    geo = geo_span.attr('title')
                urls = []
                for link in tweetPQ("a"):
                    try:
                        urls.append((link.attrib["data-expanded-url"]))
                    except KeyError:
                        pass

                tweet = Tweet(id=id,
                              permalink='https://twitter.com' + permalink, username=username_tweet,
                              text=txt,
                              date=datetime.datetime.fromtimestamp(date_sec),
                              formatted_date=datetime.datetime.fromtimestamp(date_sec).strftime("%a %b %d %X +0000 %Y"),
                              retweets=retweets,
                              favorites=favorites,
                              mentions=" ".join(re.compile('(@\\w*)').findall(txt)),
                              hashtags=" ".join(re.compile('(#\\w*)').findall(txt)),
                              geo=geo,
                              urls=",".join(urls),
                              author_id=user_id)

                results.append(tweet)
                results_aux.append(tweet)

                if receive_buffer and len(results_aux) >= buffer_length:
                    receive_buffer(results_aux)
                    results_aux = []

                if args.maxtweets and len(results) >= args.maxtweets:
                    active = False
                    break
        if receive_buffer and len(results_aux) > 0:

            receive_buffer(results_aux)
        print('\nTotal number of tweets obtained: ', len(results))

        return results

    @staticmethod
    def get_json_response(args, refresh_cursor, cookiejar, proxy):
        url = "https://twitter.com/i/search/timeline?f=tweets&q=%s&src=typd&%smax_position=%s"
        #creating the url
        url_get_data = ''
        if args.username is not None:
            url_get_data += ' from:' + args.username

        if args.since is not None:
            url_get_data += ' since:' + args.since

        if args.until is not None:
            url_get_data += ' until:' + args.until

        if args.query is not None:
            url_get_data += ' ' + args.query

        if args.near is not None:
            url_get_data += "&near:" + args.near + " within:" + args.within

        if args.language is not None:
            url_lang = 'l=' + args.language + '&'
        else:
            url_lang = ''
        url = url % (urllib.parse.quote(url_get_data), url_lang, refresh_cursor)
        print(url)

        headers = [
            ('Host',  "twitter.com"),
            ('User-Agent', "Mozilla/5.0 (Windows NT 4.1; Win64; x64)"),
            ('Accept', "application/json, text/javascript, */*; q=0.01"),
            ('Accept-Language', "en_UK,en-US;q=0.7,en;q=0.3"),
            ('X-Requested-With', "XMLHttpRequest"),
            ('Referer', url),
            ('Connection', "keep-alive")
        ]

        if proxy:
            opener = urllib.request.build_opener(urllib.request.ProxyHandler(
            {'http':proxy, 'https': proxy}),
            urllib.request.HTTPCookieProcessor(cookie_jar))
        else:
            opener = urllib.request.build_opener(
                urllib.request.HTTPCookieProcessor(cookiejar))
        opener.addheaders = headers

        try:
            response = opener.open(url)
            json_response = response.read()
        except:
            print("Twitter weird response. Try to see on browser: https://twitter.com/search?q=%s&src=typd" %
                  urllib.parse.quote(url_get_data))
            print("Unexpected error:", sys.exc_info()[0])
            sys.exit()
            return

        data_json = json.loads(json_response.decode('utf-8'))

        return data_json
