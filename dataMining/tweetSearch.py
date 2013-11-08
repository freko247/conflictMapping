# -*- coding: utf-8 -*-
from pattern.web import Twitter
from pattern.en import tag
from pattern.vector import KNN, count
import urllib2

twitter = Twitter(license=None, throttle=0.5)
knn = KNN()


def getSearchWords():
    '''Function that returns list of search words'''
    # Test data, we will use synonyms for war (found in nltk word net)
    words = ['war', 'conflict', 'jihad', ]
    return words


def getCountries():
    '''Function that returns list of countries
       downloaded from static url.
    '''
    url = r'https://raw.github.com/umpirsky/' \
          'country-list/master/country/cldr/en/country.csv'
    response = urllib2.urlopen(url)
    # TODO, check encoding
    data = response.read()
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
    # TODO: restrict searching on queries,results and time
    # Twitter.search() returns up to 3000 results for a search term
    # (30 queries with 100 results each, or 300 queries with 10 results each).
    # It has a limit of 150 queries per 15 minutes (each call to search()
    # counts as one query).
    results = twitter.search('%s AND %s' % (word, country),
                             start=1,
                             count=100,
                             sort='date'
                             )
    return [result.items() for result in results]
    # return tweets


def main():
    words = getSearchWords()
    countries = getCountries()
    tweets = getTweets(words[:4], countries[:20])
    return tweets


if __name__ == '__main__':
    print main()
