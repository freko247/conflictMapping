# -*- coding:utf-8 -*-
"""
Module defines methods for storing data in database.
"""
from datetime import datetime

import models


def saveTweets(db_session, tweets):
    """Function that stores tweets in database"""
    tweet = models.Tweet()
    for row_dict in tweets:
        string_date = row_dict.get('date')
        tweet_date = datetime.strptime(string_date[:19] + string_date[-5:],
                                       '%a %b %d %H:%M:%S %Y'
                                       )
        tweet.tweet_id = row_dict.get('id')
        tweet.tweet_language = row_dict.get('language')
        tweet.tweet_profile = row_dict.get('profile')
        tweet.tweet_author = row_dict.get('author')
        tweet.tweet_url = row_dict.get('url')
        tweet.tweet_text = row_dict.get('text')
        tweet.tweet_date = tweet_date
        db_session.merge(tweet)
        db_session.commit()
    return True
