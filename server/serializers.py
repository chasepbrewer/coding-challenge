import server.transactions as transactions


def widget_size_serializer(widget_size):
    return {'id': widget_size[0], 'name': widget_size[1]}


def widget_type_serializer(widget_type):
    return {'id': widget_type[0], 'name': widget_type[1]}


def widget_finish_serializer(widget_finish):
    return {'id': widget_finish[0], 'name': widget_finish[1]}


def widget_serializer(widget):
    widget_id, amount = widget
    widget_sizes = transactions.get_widget_sizes(widget_id)
    widget_finishes = transactions.get_widget_finishes(widget_id)
    widget_type = transactions.get_widget_type(widget_id)
    print(widget_type)

    return {
        'id': widget_id,
        'amount': amount,
        'sizes': [widget_size_serializer(size) for size in widget_sizes],
        'finishes': [widget_finish_serializer(finish) for finish in widget_finishes],
        'type': widget_type_serializer(widget_type),
    }


def order_widget_serializer(order_widget):
    order_id, widget_id, widget_size_id, widget_finish_id, amount = order_widget
    widget = transactions.get_widget(widget_id)
    widget_size = transactions.get_widget_size(widget_size_id)
    widget_finish = transactions.get_widget_finish(widget_finish_id)

    return {
        'order_id': order_id,
        'widget': widget_serializer(widget),
        'size': widget_size_serializer(widget_size),
        'finish': widget_finish_serializer(widget_finish),
        'amount': amount,
    }


def order_serializer(order):
    order_id, = order
    widgets = [
        order_widget_serializer(widget) for widget
        in transactions.get_order_widgets(order_id)]

    return {
        'id': order_id,
        'widgets': widgets,
    }