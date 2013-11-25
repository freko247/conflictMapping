# -*- coding: utf-8 -*-
"""
Configuration script
"""
import ConfigParser
import os


config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'conflictMapper.cfg'))

SLEEP_TIME = float(config.get('batch', 'SLEEP_TIME'))
DATABASE_LOCATION = config.get('database', 'DATABASE_LOCATION')
DEBUG_PORT = config.get('web server', 'DEBUG_PORT')
SERVER_PORT = config.get('web server', 'SERVER_PORT')
