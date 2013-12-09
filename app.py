# -*- coding:utf-8 -*-
"""
This script starts a Tornado Web Server, that hosts a web application,
that visualises gathered data.

Usage:
  app.py
  app.py debug
"""
from json import dumps
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import time
import signal

from docopt import docopt
from jinja2 import Environment, FileSystemLoader
# from sphinx.websupport import WebSupport
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

import config
from database import db
from database.models import Tweet

stat_dir = os.path.join(os.path.dirname(__file__), config.STAT_DIR)
template_dir = os.path.join(os.path.dirname(__file__), config.TEMPLATE_DIR)

logger = None
server = None


class Application(tornado.web.Application):
    """
    Application class, handlers and database connection are set up when
    initialized.
    """
    def __init__(self, debug):
        handlers = [(r"/", MainHandler),
                    (r'/download/(.*)',
                     tornado.web.StaticFileHandler,
                     {'path': stat_dir}),
                    ]
        settings = {'debug': debug,
                    'template_path': template_dir,
                    'static_path': stat_dir,
                    }
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=db.init_db(
                                 config.DATABASE_LOCATION)))


class MainHandler(tornado.web.RequestHandler):
    """
    Main handler class, this is the index page of the Application.
    """
    @property
    def db(self):
        """
        Returns datbase session, this is used so that same session can be
        re-used.
        """
        return self.application.db

    def get(self):
        """
        Method that is run when GET request is received from a client, ie. this
        is where the page content is rendered.

        jinja2 is used for templating, the template index.html is rendered with
        a dictionary of values that are used in the template.
        """
        # Total count of tweets
        tweets_count = self.db.query(func.count(Tweet.tweet_id)).all()
        # Tweets grouped by tweet_country with count
        tweets_country = self.db.query(Tweet.tweet_country,
                                       func.count(Tweet.tweet_id)).\
                                       group_by(Tweet.tweet_country).all()
        tweets_country = sorted(tweets_country,
                                key=lambda tup: tup[1],
                                reverse=True)
        # Tweets grouped by tweet_search_word with count
        tweets_word = self.db.query(Tweet.tweet_search_word,
                                    func.count(Tweet.tweet_id)).\
                                    group_by(Tweet.tweet_search_word).all()
        tweets_word = sorted(tweets_word,
                             key=lambda tup: tup[1],
                             reverse=True)
        # Date of newest tweet
        # tweets_newest = self.db.query(func.max(Tweet.tweet_date)).all()
        # Date of oldest tweet
        # tweets_oldest = self.db.query(func.min(Tweet.tweet_date)).all()
        # Document links
        links = [('documentation', os.path.join('download',
                                                'html_doc.7z')),
                 ('git', 'https://github.com/freko247/conflictMapping'),
                 ]
        contents = {'links': links,
                    'tweets_count': tweets_count[0][0],
                    'tweets_country': dumps(dict(tweets_country)),
                    'tweets_max': dumps(tweets_country[0][1]),
                    # 'tweets_oldest': tweets_oldest[0][0].isoformat(),
                    # 'tweets_word': tweets_word,
                    }
        try:
            env = Environment(loader=FileSystemLoader(template_dir))
            template = env.get_template('index.html')
            self.write(template.render(contents))
        except:
            logger.exception('Exception caught!')


def sig_handler(sig, frame):
    """
    Method that handles received signals.
    """
    logger.warning('Caught signal: %s', sig)
    tornado.ioloop.IOLoop.instance().add_callback(shutdown)


def shutdown():
    """
    Method shuts down server when all existings requests have been processed,
    or after maximum interval (set in configuration file).
    """
    logger.info('Stopping http server')
    server.stop()

    logger.info('Will shutdown in %s seconds ...',
                config.WAIT_SECONDS_BEFORE_SHUTDOWN)
    io_loop = tornado.ioloop.IOLoop.instance()

    deadline = time.time() + config.WAIT_SECONDS_BEFORE_SHUTDOWN

    def stop_loop():
        """
        Stop loop, checks for incoming requests and tries to shut down server.
        """
        now = time.time()
        if now < deadline and (io_loop._callbacks or io_loop._timeouts):
            io_loop.add_timeout(now + 1, stop_loop)
        else:
            io_loop.stop()
            logger.info('Shutdown')
    stop_loop()


def main(arguments):
    # TODO: Add script that builds new documentation?
    logHandler = TimedRotatingFileHandler(os.path.join(
                                          os.path.dirname(__file__),
                                          "logs", "app.log"), when="midnight")
    logFormatter = logging.Formatter('%(asctime)s: %(levelname)s; %(message)s')
    logHandler.setFormatter(logFormatter)
    global logger
    logger = logging.getLogger('app logger')
    logger.addHandler(logHandler)
    logger.setLevel(logging.DEBUG)

    debug = arguments.get('debug')
    if debug:
        port = config.DEBUG_PORT
        logger.info('Starting server in debug mode!')
        print 'Starting server in debug mode!'
    else:
        port = config.SERVER_PORT
        logger.info('Starting server!')
    logger.info('Tornado server ready at 127.0.0.1:%s (PID: %s)' %
                (port, os.getpid()))
    global server
    application = Application(debug=debug)
    server = tornado.httpserver.HTTPServer(application)
    server.listen(port)
    signal.signal(signal.SIGTERM, sig_handler)
    signal.signal(signal.SIGINT, sig_handler)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == ("__main__"):
    arguments = docopt(__doc__)
    main(arguments)
