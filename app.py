import os

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from dotenv import load_dotenv, find_dotenv

import server.views as views

load_dotenv(find_dotenv())

SETTINGS = {
    'static_path': os.path.join(os.path.dirname(__file__), '/server/static/'),
    'cookie_secret': os.environ.get('CODING_CHALLENGE_COOKIE_SECRET', 'secret'),
    'xsrf_cookies': True
}

URLS = [
    (r'/api/v1/widgets/([0-9]+)/', views.WidgetHandler),
    (r'/api/v1/widgets/', views.WidgetListHandler),
    (r'/api/v1/widgets/types/', views.WidgetTypeListHandler),
    (r'/api/v1/widgets/sizes/', views.WidgetSizeListHandler),
    (r'/api/v1/widgets/finishes/', views.WidgetFinishListHandler),
    (r'/api/v1/orders/', views.OrderListHandler)
]

if __name__ == '__main__':
    application = Application(URLS, **SETTINGS)
    server = HTTPServer(application)
    server.listen(8000)
    IOLoop.instance().start()
