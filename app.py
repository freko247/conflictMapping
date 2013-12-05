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
import sys

from docopt import docopt
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
# from sphinx.websupport import WebSupport
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import func
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


class TemplateRendering:
    """TemplateRendering
       A simple class to hold methods for rendering templates.
    """
    def render_template(self, template_name, variables):
        """render_template
            Returns the result of template.render to be used elsewhere.
            I think this will be useful to render templates to be passed into
            other templates.

            Gets the template directory from app settings dictionary
            with a fall back to "templates" as a default.

            Probably could use a default output if a template isn't found
            instead of throwing an exception.
        """
        template_dirs = []
        if self.settings["templates"] and self.settings["templates"] != '':
            template_dirs.append(os.path.join(os.path.dirname(__file__),
                                 self.settings["templates"]))
        template_dirs.append(os.path.join(os.path.dirname(__file__),
                             'templates'))  # added a default for fail over.

        env = Environment(loader=FileSystemLoader(template_dirs))

        try:
            template = env.get_template(template_name)
        except TemplateNotFound:
            raise TemplateNotFound(template_name)
        content = template.render(variables)
        return content


class Application(tornado.web.Application):
    """
    Application class, handlers and database connection are set up when
    initialized.
    """
    def __init__(self, debug):
        # html_dir = os.path.join(os.path.dirname(__file__), config.HTML_DIR)
        # stat_dir = os.path.join(os.path.dirname(__file__), config.STAT_DIR)
        handlers = [(r"/", MainHandler),
                    # (r"/doc", DocHandler),
                    ]
        settings = {'debug': debug,
                    # 'template_path': html_dir,
                    # 'static_path': stat_dir,
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
        result = self.db.query(func.count(Tweet.tweet_id)).all()
        self.write("<br> %s number of tweets about conflicts in database"
                   % result)
        result = self.db.query(Tweet.tweet_country,
                               Tweet.tweet_search_word,
                               func.count(Tweet.tweet_id)).\
                               group_by(Tweet.tweet_country,
                                        Tweet.tweet_search_word).all()
        for row in sorted(result, key=lambda tup: tup[2], reverse=True):
            country, word, count = row
            try:
                self.write('%s %s %s <br>' % (country, word, count))
            except:
                print sys.exc_info()[0]


# class DocHandler(tornado.web.RequestHandler, TemplateRendering):
#     def get(self):
#         root = os.path.dirname(__file__)
#         support = WebSupport(datadir=os.path.join(root, 'doc'),
#                              search='xapian')
#         contents = support.get_document('')
#         # a bunch of variables to pass into the template
#         content = self.render_template('doc.html', contents)
#         self.write(content)


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
