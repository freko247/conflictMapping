# -*- coding:utf-8 -*-
"""
Module defines methods for storing data in database.
"""
from hashlib import sha1
from datetime import datetime
from models import Tweet
import db


db.init_db()


def saveTweets(tweets):
    """Function that stores tweets in database"""
    # TODO: Nose tests
    tweet = Tweet()
    for row_dict in tweets:
        string_date = row_dict.get('date')
        tweet_date = datetime.strptime(string_date[:19]+string_date[-5:],
                                       '%a %b %d %H:%M:%S %Y'
                                       )
        tweet.tweet_id = row_dict.get('id')
        tweet.tweet_language = row_dict.get('language')
        tweet.tweet_profile = row_dict.get('profile')
        tweet.tweet_author = row_dict.get('author')
        tweet.tweet_url = row_dict.get('url')
        tweet.tweet_text = row_dict.get('text')
        tweet.tweet_date = tweet_date
        db.db_session.merge(tweet)
        db.db_session.commit()


def main():
    """Main function used when running script independently.
    Test data 'tweets' has expected data format"""
    tweets = [[{u'profile': u'http://pbs.twimg.com/profile_images/'
                '378800000625405614/'
                '881510dae4b7d1a9525d205106c69118_normal.jpeg',
                u'language': u'en',
                u'author': u'BarootiShahabeh',
                u'url': u'https://twitter.com/BarootiShahabeh/status/'
                '403471725436076032',
                u'text': u"RT @AlMonitor: As the #Syria war continues,"
                " Assad'sopponents are incredibly becoming lawless"
                " criminals - http://t.co/eNuTnxnW2P",
                'tweet_country': 'syria',
                u'date': u'Thu Nov 21 10:35:30 +0000 2013',
                'tweet_search_word': 'war',
                u'id': u'403471725436076032'}], ]
    saveTweets(tweets)
    return


if __name__ == '__main__':
    main()
