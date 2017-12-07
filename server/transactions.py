import os.path as path

from sqlite3 import connect

conn = connect(path.join(path.dirname(__file__), '../data.db'))


def get_widget_list(widget_type=None, size=None, finish=None):
    """
    Returns a list of widgets matching the given search filters.
    :param widget_type: int or None
    :param size: int or None
    :param finish: int or None
    :return: list of (int, int)
    """
    query = 'select id, amount from widgets'
    c = conn.cursor()

    if not widget_type and not size and not finish:
        return c.execute(query)

    filters = []

    if widget_type:
        filters.append('id = :type')

    if size:
        filters.append('id in (select widget_id from widget_size_map '
                       'where widget_size_id = :size)')

    if finish:
        filters.append('id in (select widget_id from widget_finish_map where '
                       'widget_finish_id = :finish)')

    query += ' where {}'.format(' AND '.join(filters))

    c.execute(query, {
        'type': widget_type,
        'size': size,
        'finish': finish,
    })

    return c.fetchall()


def get_widget(widget_id):
    """
    Returns a widget by it's id.
    :param widget_id: int
    :return: (int, int)
    """
    c = conn.cursor()
    c.execute('select id, amount from widgets where id = ?', (widget_id,))

    return c.fetchone()


def get_widget_finishes(widget_id):
    """
    Returns widget finishes associated with a particular widget.
    :param widget_id: int
    :return: list of (int, string)
    """
    c = conn.cursor()
    c.execute('select id, name from widget_finishes where id in '
              '(select widget_size_id from widget_size_map where '
              'widget_id = ?)', (widget_id,))

    return c.fetchall()


def get_widget_finish(widget_finish_id):
    """
    Returns a widget_finish by it's id.
    :param widget_finish_id: int
    :return: (int, string)
    """
    c = conn.cursor()
    c.execute('select id, name from widget_finishes where '
              'id = ?', (widget_finish_id,))

    return c.fetchone()


def get_widget_finish_list():
    """
    Returns all the current widget finishes.
    :return: list of (int, string)
    """
    c = conn.cursor()
    c.execute('select id, name from widget_finishes')

    return c.fetchall()


def get_widget_size_list():
    """
    Returns all the currenet widget sizes.
    :return: list of (int, string)
    """
    c = conn.cursor()
    c.execute('select id, name from widget_sizes')

    return c.fetchall()


def get_widget_sizes(widget_id):
    """
    Returns widget sizes associated with a widget.
    :param widget_id: int
    :return: list of (int, string)
    """
    c = conn.cursor()
    c.execute('select id, name from widget_sizes where id in '
              '(select widget_size_id from widget_size_map where '
              'widget_id = ?)', (widget_id,))

    return c.fetchall()


def get_widget_size(widget_size_id):
    """
    Returns a widget size by it's id.
    :param widget_size_id: int
    :return: (int, string)
    """
    c = conn.cursor()
    c.execute('select id, name from widget_sizes where '
              'id = ?', (widget_size_id,))

    return c.fetchone()


def get_widget_type_list():
    """
    Returns all the current widget types.
    :return: list of (int, string)
    """
    c = conn.cursor()
    c.execute('select widget_id, name from widget_types')

    return c.fetchall()


def get_widget_type(widget_id):
    """
    Returns a widget type associated with a widget.
    :param widget_id: int
    :return: (int, string)
    """
    c = conn.cursor()
    c.execute('select widget_id, name from widget_types where '
              'widget_id = ?', (widget_id,))

    return c.fetchone()


def get_order_list():
    """
    Returns all the current orders.
    :return: list of (int)
    """
    c = conn.cursor()
    c.execute('select id from orders')

    return c.fetchall()


def get_order_widgets(order_id):
    """
    Gets the widgets associated with an order.
    :return: list of (int, int, int, int, int)
    """
    c = conn.cursor()
    c.execute('select id, order_id, widget_id, widget_size_id, '
              'widget_finish_id, amount from order_widgets '
              'where order_id = ?', (order_id,))

    return c.fetchall()


def create_order():
    """
    Creates an order.
    :return: int
    """
    c = conn.cursor()
    c.execute('insert into orders default values')

    return c.lastrowid

def get_order(order_id):
    """
    Gets an order by it's id.
    :param order_id: int
    :return: (int) or None
    """
    c = conn.cursor()
    c.execute('select id from orders where id = ?', order_id)

    return c.fetchone()


def delete_order(order_id):
    """
    Deletes an order
    :param order_id: int
    """
    c = conn.cursor()
    c.execute('delete from order_widgets where order_id = ?', order_id)
    c.execute('delete from orders where id = ?', order_id)


def get_order_widget(order_widget_id):
    """

    :param order_widget_id:
    :return:
    """
    c = conn.cursor()
    c.execute('select id, order_id, widget_id, widget_size_id, '
              'widget_finish_id, amount from order_widgets where '
              'id = ?', (order_widget_id,))

    return c.fetchone()


def add_widget_to_order(
        order_id, widget_id, widget_size_id,
        widget_finish_id, amount=1):
    """
    Adds a widget to an order. If the widget already exists on the order,
    update the amount.
    :param order_id: int
    :param widget_id: int
    :param widget_size_id: int
    :param widget_finish_id: int
    :param amount: int
    :return: int
    """
    c = conn.cursor()
    order_widget = (
        order_id, widget_id, widget_size_id, widget_finish_id, amount)
    c.execute('select id, amount from order_widgets where order_id = ? and '
              'widget_id = ? and widget_size_id = ? and '
              'widget_finish_id = ?',
              (order_id, widget_id, widget_size_id, widget_finish_id,))

    matching_widget = c.fetchone()

    if matching_widget:
        order_widget_id, current_amount = matching_widget
        new_amount = current_amount + amount
        c.execute('update order_widgets set amount = ? '
                  'where id = ?', (new_amount, order_widget_id))
    else:
        c.execute('insert into order_widgets (order_id, widget_id, '
                  'widget_size_id, widget_finish_id, amount) values '
                  '(?, ?, ?, ?, ?)', order_widget)

    return c.lastrowid


def remove_widget_from_order(order_widget_id):
    """
    Removes a widget from an order.
    :param order_widget_id: int
    """
    c = conn.cursor()
    c.execute('delete from order_widgets where id = ?', (order_widget_id,))
