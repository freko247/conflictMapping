# -*- coding: utf-8 -*-
"""
Batch script that retrieves and stores tweets in database
"""
import logging
import os
import time

from sqlalchemy.orm import scoped_session, sessionmaker
from pattern.web import SearchEngineLimitError

import config
from dataMining import tweetSearch
from database import db, db_functions


def main():
    """
    Main function in batch script, where eternal while loop is running.

    Script uses modules dataMining and database to retrieve and store data.
    """
    logging.basicConfig(filename='logs/batch.log',
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s')
    countries = tweetSearch.getCountries()
    words = tweetSearch.getSearchWords()
    start_time = time.time()
    create_tables = False
    if not os.path.isfile(config.DATABASE_LOCATION):
        create_tables = True
    engine = db.init_db(config.DATABASE_LOCATION)
    if create_tables:
        db.create_tables(engine)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    while 1:
        start_time = time.time()
        for word in words:
            for country in countries:
                try:
                    tweets = tweetSearch.getTweets(word, country)
                except SearchEngineLimitError:
                    run_time = time.time() - start_time
                    logging.warning('Quota exceded, sleeping for %s seconds' %
                                    (3600 - run_time))
                    time.sleep(3600 - run_time)
                    tweets = tweetSearch.getTweets(word, country)
                # Save tweets
                logging.debug('Found %s tweets when searching for %s + %s.' %
                              (len(tweets), word, country))
                db_functions.saveTweets(db_session, tweets)

if __name__ == '__main__':
    main()
