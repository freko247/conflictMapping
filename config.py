# -*- coding: utf-8 -*-
"""
Configuration script
"""
import ConfigParser

config = ConfigParser.RawConfigParser()
config.read('conflictMapper.cfg')

DATABASE_LOCATION = config.get('database', 'DATABASE_LOCATION')
