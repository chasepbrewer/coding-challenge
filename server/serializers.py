"""
Utility functions that transform database objects into JSON serializable
dictionaries.
"""

import server.transactions as transactions


def widget_size_serializer(widget_size):
    """
    Serializes a widget_size object.
    :param widget_size: (int, string)
    :return: dict
    """
    return {'id': widget_size[0], 'name': widget_size[1]}


def widget_type_serializer(widget_type):
    """
    Serializes a widget_type object.
    :param widget_type: (int, string)
    :return: dict
    """
    return {'id': widget_type[0], 'name': widget_type[1]}


def widget_finish_serializer(widget_finish):
    """
    Serializes a widget_finish object.
    :param widget_finish: (int, string)
    :return: dict
    """
    return {'id': widget_finish[0], 'name': widget_finish[1]}


def widget_serializer(widget):
    """
    Serializes a widget object.
    :param widget: (int, int)
    :return: dict
    """
    widget_id, amount = widget
    widget_sizes = transactions.get_widget_sizes(widget_id)
    widget_finishes = transactions.get_widget_finishes(widget_id)
    widget_type = transactions.get_widget_type(widget_id)

    return {
        'id': widget_id,
        'amount': amount,
        'sizes': [widget_size_serializer(size) for size in widget_sizes],
        'finishes': [widget_finish_serializer(finish) for finish in widget_finishes],
        'type': widget_type_serializer(widget_type),
    }


def order_widget_serializer(order_widget):
    """
    Serializes an order_widget object.
    :param order_widget: (int, int, int, int, int, int)
    :return: dict
    """
    id = order_widget[0]
    order_id = order_widget[1]
    widget_id = order_widget[2]
    widget_size_id = order_widget[3]
    widget_finish_id = order_widget[4]
    amount = order_widget[5]
    widget = transactions.get_widget(widget_id)
    widget_size = transactions.get_widget_size(widget_size_id)
    widget_finish = transactions.get_widget_finish(widget_finish_id)

    return {
        'id': id,
        'order_id': order_id,
        'widget': widget_serializer(widget),
        'size': widget_size_serializer(widget_size),
        'finish': widget_finish_serializer(widget_finish),
        'amount': amount,
    }


def order_serializer(order):
    """
    Serializes an order object.
    :param order: (int)
    :return: dict
    """
    order_id, = order
    widgets = [
        order_widget_serializer(widget) for widget
        in transactions.get_order_widgets(order_id)]

    return {
        'id': order_id,
        'widgets': widgets,
    }