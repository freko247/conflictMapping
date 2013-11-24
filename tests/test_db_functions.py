# -*- coding: utf-8 -*-
"""
Module for testing database.db_functions.py
"""
from sqlalchemy.orm import scoped_session, sessionmaker
# TODO: Fix this import, it's ugly
from ..database import db, db_functions

# TODO: Move to 'test setup'
engine = db.init_db('test_lite.db')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))

# TODO: Use fixtures instead for test data
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
           u'id': u'403471725436076032'}, ]


def test_saveTweets():
    # TODO: Move to 'test setup'
    db.create_tables(engine)
    # TODO: Make test more complicated
    assert db_functions.saveTweets(db_session, tweets)
    # TODO: Add test tear down (eg. delete test db)
