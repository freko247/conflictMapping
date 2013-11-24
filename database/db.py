# -*- coding:utf-8 -*-
"""
Module used for initiating database connection.
Sqlite database named lite.db is created by default.
"""
from sqlalchemy import create_engine
import models


def create_tables(engine):
    """
    Database creation.
    """
    models.DeclarativeBase.metadata.create_all(engine)


def init_db(db_location='lite.db'):
    """
    Database initialization.
    """
    return create_engine('sqlite:///%s' % db_location)
