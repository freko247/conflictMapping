from sqlalchemy import Column, DateTime, String
from db import Base


class Tweet(Base):
    """Database model for tweet table"""
    __tablename__ = 'tweet'
    tweet_id = Column(String, primary_key=True)
    tweet_language = Column(String)
    tweet_profile = Column(String,)
    tweet_author = Column(String,)
    tweet_url = Column(String,)
    tweet_text = Column(String,)
    tweet_date = Column(DateTime,)
    tweet_country = Column(String,)
    tweet_search_word = Column(String,)
