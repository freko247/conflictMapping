# -*- coding:utf-8 -*-
"""
Tornado web server, hosts page that visualises tweet data.

Usage:
  app.py
  app.py debug
"""
import logging
from logging.handlers import TimedRotatingFileHandler
import os
import time
import signal

from docopt import docopt
from sqlalchemy.orm import scoped_session, sessionmaker
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web

from database import db
from database.models import Tweet
import config


MAX_WAIT_SECONDS_BEFORE_SHUTDOWN = 3

logger = None
server = None


class Application(tornado.web.Application):
    """
    Application class, handlers and database connection are set up when
    initialized.
    """
    def __init__(self, debug):
        handlers = [(r"/", MainHandler), ]
        settings = {'debug': debug
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
        """
        self.write("conflictMapping")
        tweets = self.db.query(Tweet).all()
        self.write("<br> %s number of tweets about conflicts in database"
                   % len(tweets))


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
    logHandler = TimedRotatingFileHandler(os.path.join(
                                          os.path.dirname(__file__),
                                          "logs", "app.log"), when="midnight")
    logFormatter = logging.Formatter('%(asctime)s: %(levelname)s; %(message)s')
    logHandler.setFormatter(logFormatter)
    global logger
    logger = logging.getLogger('app logger')
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)

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
