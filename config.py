# -*- coding: utf-8 -*-
"""
Configuration script
"""
import ConfigParser
import os


config = ConfigParser.RawConfigParser()
config.read(os.path.join(os.path.dirname(__file__), 'conflictMapping.cfg'))

# Batch
SLEEP_TIME = float(config.get('batch', 'SLEEP_TIME'))

# Database
DATABASE_LOCATION = os.path.join(os.path.dirname(__file__),
                                 config.get('database', 'DATABASE_LOCATION')
                                 )

# Web server
DEBUG_PORT = config.get('web server', 'DEBUG_PORT')
DOC_DIR = config.get('web server', 'DOC_DIR')
HTML_DIR = config.get('web server', 'HTML_DIR')
WAIT_SECONDS_BEFORE_SHUTDOWN = float(config.get('web server',
                                                'WAIT_SECONDS_BEFORE_SHUTDOWN'
                                                ))
SERVER_PORT = config.get('web server', 'SERVER_PORT')
