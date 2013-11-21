# -*- coding: utf-8 -*-
"""
Database models.
"""
from sqlalchemy import Column, DateTime, String
from db import Base


class Tweet(Base):
    """Database model for tweet table"""
    __tablename__ = 'tweet'
    tweet_id = Column(String, primary_key=True, doc='Unique ID of tweet')
    tweet_language = Column(String, doc='Author language')
    tweet_profile = Column(String, doc='Link to author profile picture')
    tweet_author = Column(String, doc='Author user name')
    tweet_url = Column(String, doc='Permalink to tweet')
    tweet_text = Column(String, doc='Tweet text')
    tweet_date = Column(DateTime, doc='Date and time of tweet')
    tweet_country = Column(String, doc='Search: country')
    tweet_search_word = Column(String, doc='Search: word')
