# -*- coding: utf-8 -*-
"""
Configuration script
"""
import ConfigParser
import os

root = os.path.dirname(__file__)

config = ConfigParser.RawConfigParser()
config.read(os.path.join(root, 'conflictMapping.cfg'))

# Batch
SLEEP_TIME = float(config.get('batch', 'SLEEP_TIME'))

# Database
DATABASE_LOCATION = os.path.join(root,
                                 config.get('database', 'DATABASE_LOCATION')
                                 )

# Web server
DEBUG_PORT = config.get('web server', 'DEBUG_PORT')
SERVER_PORT = config.get('web server', 'SERVER_PORT')
STAT_DIR = os.path.join(root, config.get('web server', 'STAT_DIR'))
TEMPLATE_DIR = os.path.join(root, config.get('web server', 'TEMPLATE_DIR'))
WAIT_SECONDS_BEFORE_SHUTDOWN = float(config.get('web server',
                                                'WAIT_SECONDS_BEFORE_SHUTDOWN'
                                                ))
