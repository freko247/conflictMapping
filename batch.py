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
    logger.info('Started script (PID: %s).' % os.getpid())
    # Starting datamining loop
    while 1:
        for word in words:
            for country in countries:
                tweets = None
                while not tweets:
                    try:
                        tweets = tweetSearch.getTweets(word, country)
                    except SearchEngineLimitError:
                        logger.warning('Search engine limit exceded,'
                                       ' sleeping for %s seconds.' %
                                       config.SLEEP_TIME)
                        time.sleep(config.SLEEP_TIME)
                # Save tweets
                logger.info('Found %s tweets when searching for %s + %s.' %
                            (len(tweets), word, country))
                db_functions.saveTweets(db_session, tweets)

if __name__ == '__main__':
    main()
