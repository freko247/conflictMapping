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
    # words = ['war', 'conflict', 'jihad', ]
    words = []
    conflict = ['feud',
                'vendetta',
                'class struggle',
                'strife',
                'countercurrent',
                'discord',
                'trench warfare',
                'fight',
                'hassle',
                'beating',
                'in fighting',
                'single combat',
                'gunfight',
                'battering',
                'knife fight',
                'affray',
                'turf war',
                'rebellion',
                'intifada',
                'insurgency',
                ]
    military_action = ['saber rattling',
                       'battle',
                       'assault'
                       'naval battle',
                       'combat',
                       'pitched_battle',
                       'amphibious_landing',
                       'police action',
                       'war',
                       'psychological warfare',
                       'information warfare',
                       'limited war',
                       'jihad',
                       'chemical warfare',
                       'civil war',
                       'biological warfare',
                       'world war',
                       'electronic warfare',
                       'blockade',
                       'siege',
                       'naval blockade',
                       'defense',
                       'chemical defense',
                       'hasty defense',
                       'biological warfare defense',
                       'air defense',
                       'deliberate defense',
                       'biological defense',
                       ]
    war = ['psychological warfare',
           'information warfare',
           'limited war',
           'jihad',
           'chemical warfare',
           'hot_war',
           'civil_war',
           'biological warfare',
           'germ_warfare',
           'world war',
           ]
    words.extend(conflict)
    words.extend(military_action)
    words.extend(war)
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


def getTweets(terms):
    """
    Expects a tuple/list of strings as parameter.

    Method then searches for tweets containing the  from Twitter using
    the package 'pattern'.

    Search with the API is restricted on number of queries, results and time.
    Twitter.search() returns up to 3000 results for a search term,
    (30 queries with 100 results each, or 300 queries with 10 results each).
    The API has a limit of 150 queries per 15 minutes (each call to search()
    counts as one query).
    """
    print ' AND '.join(terms)
    return twitter.search(' AND '.join(terms),
                          start=1,
                          count=100,
                          sort='date'
                          )


def main():
    """
    Main function, used for testing.
    """
    # words = getSearchWords()
    # countries = getCountries()
    tweets = getTweets([('war', 'syria'), ])
    print tweets


if __name__ == '__main__':
    main()
