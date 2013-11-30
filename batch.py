# -*- coding: utf-8 -*-
"""
Batch script that retrieves and stores tweets in database
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import time
import signal
import sys

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
    # Logger
    logHandler = TimedRotatingFileHandler(os.path.join(
                                          os.path.dirname(__file__),
                                          "logs", "batch.log"),
                                          when="midnight")
    logFormatter = logging.Formatter('%(asctime)s: %(levelname)s; %(message)s')
    logHandler.setFormatter(logFormatter)
    logger = logging.getLogger('batch logger')
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

    # Signals
    def signal_handler(sig, frame):
        """
        Method that handles received kill signals.
        """
        logger.warning('Caught signal: %s, killing process.', sig)
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    # Search setup
    countries = tweetSearch.getCountries()
    words = tweetSearch.getSearchWords()
    # Database setup
    create_tables = False
    if not os.path.isfile(config.DATABASE_LOCATION):
        create_tables = True
    engine = db.init_db(config.DATABASE_LOCATION)
    if create_tables:
        db.create_tables(engine)
    db_session = scoped_session(sessionmaker(autocommit=False,
                                             autoflush=False,
                                             bind=engine))
    print 'created db'
    logger.info('Started script (PID: %s).' % os.getpid())

    def get_and_store_data(search_terms, search_function, save_function):
        """
        Method used when getting and storing data. Method is made in a
        semi-generic manner, so that it the batch script can evolve into
        a dynamic script that can be tailored in the configuration file.
        """
        skipped_terms = []
        for terms in search_terms:
            results = None
            try:
                print 'getting tweets'
                results = search_function(terms)
            except SearchEngineLimitError:
                logger.warning('Search engine limit exceeded,'
                               ' sleeping for %s seconds.' %
                               config.SLEEP_TIME)
                time.sleep(config.SLEEP_TIME)
                skipped_terms.append(terms)
            if results:
                # Save tweets
                logger.info('Found %s results when searching for %s.' %
                            (len(results), ' and '.join(terms)))
                save_function(db_session, results, terms)
        if skipped_terms:
            get_and_store_data(skipped_terms,
                               search_function,
                               save_function)
    # Starting datamining loop
    while 1:
        search_terms = [(a, b) for b in words for a in countries]
        search_function = tweetSearch.getTweets
        save_function = db_functions.saveTweets
        get_and_store_data(search_terms, search_function, save_function)

if __name__ == '__main__':
    main()
