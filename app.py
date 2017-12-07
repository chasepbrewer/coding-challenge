import os

from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application
from dotenv import load_dotenv, find_dotenv

import server.views as views

load_dotenv(find_dotenv())

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

SETTINGS = {
    'static_path': os.path.join(PROJECT_ROOT, 'server/static'),
    'template_path': os.path.join(PROJECT_ROOT, 'server/templates'),
    'cookie_secret': os.environ.get('CODING_CHALLENGE_COOKIE_SECRET', 'secret'),
    'xsrf_cookies': True
}

URLS = [
    (r'/', views.IndexPage),
    (r'/api/v1/widgets/([0-9]+)/', views.WidgetAPIHandler),
    (r'/api/v1/widgets/', views.WidgetListAPIHandler),
    (r'/api/v1/widgets/types/', views.WidgetTypeListAPIHandler),
    (r'/api/v1/widgets/sizes/', views.WidgetSizeListAPIHandler),
    (r'/api/v1/widgets/finishes/', views.WidgetFinishListAPIHandler),
    (r'/api/v1/orders/', views.OrderListAPIHandler),
    (r'/api/v1/orders/([0-9]+)/', views.OrderAPIHandler),
    (r'/api/v1/orders/([0-9]+)/widgets/', views.OrderWidgetListAPIHandler),
    (r'/api/v1/orders/widgets/([0-9]+)/', views.OrderWidgetAPIHandler)
]

if __name__ == '__main__':
    application = Application(URLS, **SETTINGS)
    server = HTTPServer(application)
    server.listen(8000)
    IOLoop.instance().start()
