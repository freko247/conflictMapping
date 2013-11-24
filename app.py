# -*- coding:utf-8 -*-
"""
Tornado web server, hosts page that visualises tweet data.

Usage:
  app.py
  app.py debug
"""

from sqlalchemy.orm import scoped_session, sessionmaker
import tornado.ioloop
import tornado.web
from docopt import docopt

from database import db
from database.models import Tweet
import config


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


if __name__ == ("__main__"):
    arguments = docopt(__doc__)
    debug = arguments.get('debug')
    if debug:
        port = config.get('web server', 'DEBUG_PORT')
        print 'Starting server in debug mode!'
    else:
        port = config.get('web server', 'DEBUG_PORT')
        print 'Starting server!'
    print 'Tornado server ready at 127.0.0.1:%s' % port
    application = Application(debug=debug)
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()
