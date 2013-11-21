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

from database.db import engine
from database.models import Tweet


class Application(tornado.web.Application):
    def __init__(self, debug):
        handlers = [(r"/", MainHandler), ]
        settings = {'cookie_secret': 'some_long_secret_and_other_settins',
                    'debug': debug}
        tornado.web.Application.__init__(self, handlers, **settings)
        self.db = scoped_session(sessionmaker(bind=engine))


class MainHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    def get(self):
        self.write("conflictMapping")
        tweets = self.db.query(Tweet).all()
        self.write("<br> %s number of tweets about conflicts in database"
                   % len(tweets))


if __name__ == ("__main__"):
    arguments = docopt(__doc__)
    debug = arguments.get('debug')
    if debug:
        print 'Starting in debug mode!'
    else:
        'Starting server!'
    application = Application(debug=debug)
    application.listen(8889)
    tornado.ioloop.IOLoop.instance().start()
