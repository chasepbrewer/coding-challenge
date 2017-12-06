from tornado.web import RequestHandler
from tornado.escape import json_decode, json_encode

import server.transactions as transactions
import server.serializers as serializers


class WidgetListAPIHandler(RequestHandler):
    def get(self):
        widget_type = self.get_argument('type', None)
        size = self.get_argument('size', None)
        finish = self.get_argument('finish', None)
        widgets = transactions.get_widget_list(widget_type, size, finish)
        serialized_widgets = [
            serializers.widget_serializer(widget) for widget
            in widgets]

        self.write(json_encode(serialized_widgets))


class WidgetTypeListAPIHandler(RequestHandler):
    def get(self):
        widget_types = transactions.get_widget_type_list()
        serialized_widget_types = [
            serializers.widget_type_serializer(widget_type)
            for widget_type in widget_types]

        self.write(json_encode(serialized_widget_types))


class WidgetSizeListAPIHandler(RequestHandler):
    def get(self):
        widget_sizes = transactions.get_widget_size_list()
        serialized_widget_sizes = [
            serializers.widget_size_serializer(widget_size)
            for widget_size in widget_sizes]

        self.write(json_encode(serialized_widget_sizes))


class WidgetAPIHandler(RequestHandler):
    def get(self, widget_id):
        widget = transactions.get_widget(widget_id)

        if not widget:
            self.send_error(404)

        self.write(json_encode(serializers.widget_serializer(widget)))


class WidgetFinishListAPIHandler(RequestHandler):
    def get(self):
        widget_finishes = transactions.get_widget_finish_list()
        serialised_widget_finishes = [
            serializers.widget_finish_serializer(widget_finish)
            for widget_finish in widget_finishes]

        self.write(json_encode(serialised_widget_finishes))


class OrderListAPIHandler(RequestHandler):
    def get(self):
        orders = transactions.get_order_list()
        serialized_orders = [
            serializers.order_serializer(order) for order
            in orders]

        self.write(json_encode(serialized_orders))

    def post(self):
        data = json_decode(self.request.body)
        print(data)


class IndexPage(RequestHandler):
    def get(self):
        self.render('index.html', xsrf_token=self.xsrf_token)
