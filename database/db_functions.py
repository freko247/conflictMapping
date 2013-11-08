# -*- coding:utf-8 -*-
from hashlib import sha1
from datetime import datetime
from models import Tweet
import db


db.init_db()


def generateRowDict(data):
    '''Generator that returns data row as dictionary'''
    for row in data:
        row_dict = {}
        for key, value in row:
            row_dict[key] = value
        yield row_dict


def saveTweets(tweets):
    '''Function that stores tweets in database'''
    # TODO: Nose tests
    tweet = Tweet()
    for row_dict in generateRowDict(tweets):
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
    '''Main function used when running script independently.
    Test data 'tweets' has expected data format'''
    # try:
    #     import config
    #     # TODO: Fix relative import config is in ../config/config.py
    #     # and/or move config file
    #     DATABASE_LOCATION = config.DATABASE_LOCATION
    # except ImportError:
    #     DATABASE_LOCATION = 'lite.db'
    # database = SqliteDatabase(DATABASE_LOCATION)
    # database.connect()
    tweets = [[(u'profile',
                u'http://a0.twimg.com/profile_images/2709678005/'
                'e4dfb055e127c9f1f41b90335e67e964_normal.jpeg'),
               (u'language', u'en'),
               (u'author', u'PatrakaarPopat'),
               (u'url', u'https://twitter.com/PatrakaarPopat/status/'
                '385052813715185664'),
               (u'text', u"RT @cpjasia: Journo from #Indonesia wins @AFP"
                "prize for brave reporting on #Syria's civil war and"
                " #Jakarta's drug trade. http://t.co/i0cvBP\u2026"),
               (u'date', u'Tue Oct 01 14:45:19 +0000 2013'),
               (u'id', u'385052813715185664')], ]
    saveTweets(tweets)
    return


if __name__ == '__main__':
    main()
