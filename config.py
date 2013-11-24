# -*- coding: utf-8 -*-
"""
Configuration script
"""
import ConfigParser
import os


config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'conflictMapper.cfg'))

DATABASE_LOCATION = config.get('database', 'DATABASE_LOCATION')
