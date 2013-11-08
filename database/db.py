# -*- coding:utf-8 -*-
from sqlalchemy import DateTime, Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

"""
Script used for initiating database connection.
Sqlite database named lite.db is created by default.
"""

DATABASE_LOCATION = 'lite.db'

engine = create_engine('sqlite:///%s' % DATABASE_LOCATION)
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
