# -*- coding: utf-8 -*-
"""
Batch script that retrieves and stores tweets in database
"""
import time
from dataMining import tweetSearch
from database import db_functions


def main():
    """
    Main function in batch script, where eternal while loop is running.

    Script uses modules dataMining and database to retrieve and store data.
    """
    no_queries = 0
    no_results = 0
    countries = tweetSearch.getCountries()
    words = tweetSearch.getSearchWords()
    start_time = time.time()
    while 1:
        for word in words:
            for country in countries:
                if no_queries < 600 and no_results < 3000:
                    tweets = tweetSearch.getTweets(word, country)
                    # Save tweets
                    print '%s tweets when searching for %s + %s.' % \
                        (len(tweets), word, country)
                    db_functions.saveTweets(tweets)
                    no_queries += 1
                    no_results += len(tweets)
                else:
                    run_time = time.time() - start_time
                    # Wait until full hour
                    print "Quota exceded, sleeping for %s seconds" % \
                        (3600-run_time)
                    time.sleep(3600-run_time)
                    # Reset start time, no_queries and no_results
                    start_time = time.time()
                    no_queries = 0
                    no_results = 0
            raise
if __name__ == '__main__':
    main()
