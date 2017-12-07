from tornado.web import RequestHandler
from tornado.escape import json_decode, json_encode

import server.transactions as transactions
import server.serializers as serializers


class WidgetListAPIHandler(RequestHandler):
    """
    REST API endpoint handler for widget lists.
    """
    def get(self):
        widget_type = self.get_argument('type', None)
        size = self.get_argument('size', None)
        finish = self.get_argument('finish', None)
        widgets = transactions.get_widget_list(widget_type, size, finish)
        serialized_widgets = [
            serializers.widget_serializer(widget) for widget
            in widgets]

        self.write({'results': serialized_widgets})


class WidgetTypeListAPIHandler(RequestHandler):
    """
    REST API endpoint handler for widget type lists.
    """
    def get(self):
        widget_types = transactions.get_widget_type_list()
        serialized_widget_types = [
            serializers.widget_type_serializer(widget_type)
            for widget_type in widget_types]

        self.write({'results': serialized_widget_types})


class WidgetSizeListAPIHandler(RequestHandler):
    """
    Rest API endpoint handler for widget_size lists.
    """
    def get(self):
        widget_sizes = transactions.get_widget_size_list()
        serialized_widget_sizes = [
            serializers.widget_size_serializer(widget_size)
            for widget_size in widget_sizes]

        self.write({'results': serialized_widget_sizes})


class WidgetAPIHandler(RequestHandler):
    """
    Rest API endpoint handler for a widget object.
    """
    def get(self, widget_id):
        widget = transactions.get_widget(widget_id)

        if not widget:
            self.send_error(404)

        self.write(serializers.widget_serializer(widget))


class WidgetFinishListAPIHandler(RequestHandler):
    """
    REST API endpoint handler for widget_finish lists.
    """
    def get(self):
        widget_finishes = transactions.get_widget_finish_list()
        serialised_widget_finishes = [
            serializers.widget_finish_serializer(widget_finish)
            for widget_finish in widget_finishes]

        self.write({'results': serialised_widget_finishes})


class OrderAPIHandler(RequestHandler):
    """
    REST API endpoint handler for an order object.
    """
    def get(self, order_id):
        order = transactions.get_order(order_id)

        if order:
            serialized_order = serializers.order_serializer((order_id,))
            self.write(serialized_order)
        else:
            self.set_status(404)
            self.finish()

    def delete(self, order_id):
        transactions.delete_order(order_id)

        self.finish()


class OrderListAPIHandler(RequestHandler):
    """
    REST API endpoint handler for
    """
    def get(self):
        orders = transactions.get_order_list()
        serialized_orders = [
            serializers.order_serializer(order) for order
            in orders]

        self.write({'results': serialized_orders})

    def post(self):
        order_id = transactions.create_order()
        serialized_order = serializers.order_serializer((order_id,))

        self.write(serialized_order)


class OrderWidgetAPIHandler(RequestHandler):
    def delete(self, order_id, order_widget_id):
        transactions.remove_widget_from_order(order_widget_id)

        self.finish()


class OrderWidgetListAPIHandler(RequestHandler):
    def get(self, order_id):
        order_widgets = transactions.get_order_widgets(order_id)
        serialized_order_widgets = [
            serializers.order_widget_serializer(order_widget)
            for order_widget in order_widgets]

        self.write({'results': serialized_order_widgets})

    def post(self, order_id):
        data = json_decode(self.request.body)
        widget_id = data['widget_id']
        widget_size_id = data['widget_size_id']
        widget_finish_id = data['widget_finish_id']
        amount = data['amount']
        order_widget_id = transactions.add_widget_to_order(
            order_id, widget_id, widget_size_id,
            widget_finish_id, amount)
        order_widget = transactions.get_order_widget(order_widget_id)
        serialized_order_widget = serializers.order_widget_serializer(
            order_widget)

        return self.write(serialized_order_widget)


class IndexPage(RequestHandler):
    def get(self):
        self.render('index.html', xsrf_token=self.xsrf_token)
