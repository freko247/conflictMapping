# -*- coding: utf-8 -*-
"""
Module with methods used for retreiving tweets, containing certain
search words, from Twitter.
"""
from pattern.web import Twitter
from pattern.vector import KNN
import urllib2

twitter = Twitter(license=None, throttle=0.5)
knn = KNN()


def getSearchWords():
    """Function that returns list of search words"""
    # Test data, we will use synonyms for war (found in nltk word net)
    words = ['war', 'conflict', 'jihad', ]
    return words


def getCountries():
    """Function that returns list of countries
       downloaded from static url.
    """
    url = r'https://raw.github.com/umpirsky/' \
          'country-list/master/country/cldr/en/country.csv'
    response = urllib2.urlopen(url)
    # TODO: check encoding
    data = unicode(response.read(), 'utf-8')
    country_data = data.split('\n')
    country = country_data[1]
    countries = []
    for country in country_data[1:]:
        if country:
            split_country = country.split(',')
            countries.append(split_country[1])
    # Test data
    # countries = ['Syria', 'Egypth', 'Iraq',]
    return countries  # Only get data for 20 first countries when testing


def getTweets(word, country):
    """
    Searches Twitter for tweets containing two words, 'country' and 'word',
    given as parameters.


    Usage needs to be restricted on number of queries, results and time.
    Twitter.search() returns up to 3000 results for a search term,
    (30 queries with 100 results each, or 300 queries with 10 results each).
    The API has a limit of 150 queries per 15 minutes (each call to search()
    counts as one query).
    """
    results = twitter.search('%s AND %s' % (word, country),
                             start=1,
                             count=100,
                             sort='date'
                             )
    tweets = []
    for result in results:
        tweet = {'tweet_country': country, 'tweet_search_word': word}
        tweet.update(dict(result.items()))
        tweets.append(tweet)
    return tweets


def main():
    """
    Main function, used for testing.
    """
    # words = getSearchWords()
    # countries = getCountries()
    tweets = getTweets('war', 'syria')
    print tweets


if __name__ == '__main__':
    main()
