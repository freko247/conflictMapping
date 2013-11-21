# -*- coding: utf-8 -*-
"""
Module for testing database.db_functions.py
"""
# TODO: Fix this import, it's ugly
from ..database import db_functions, models

tweets = [{u'profile': u'http://pbs.twimg.com/profile_images/'
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
               u'id': u'403471725436076032'},]

def test_saveTweets():
    assert db_functions.saveTweets(tweets)
