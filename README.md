# Coding Challenge

Built with Python, Tornado, SQLite, Vue.js, and Bootstrap.

## Dependencies

* SQLite 3.16.0
* Python 3.6.3

## Setup

Setup the SQLite database schema by running this command in the root directory:

```
$ sqlite3 data.db < setup.sql
```

Install all python dependencies by running a pip install of the given requirements file:

```
$ pip install -r requirements.txt
```

Optional: Setup a custom cookie secret to prevent XSRF attacks. Create an environment variable named `CODING_CHALLENGE_COOKIE_SECRET` either manually or by creating a file named `.env` at the root directory and placing this in it:

```
CODING_CHALLENGE_COOKIE_SECRET=yoursecretkey
```

If no cookie secret is given, a default one will be used.

Run the server by running this command:

```
$ python app.py
```

## REST API Endpoints

* `/api/v1/widgets/`: Returns a list of all the current widgets.
    * `?size=1`: Filter widgets by size.
    * `?type=1`: Filter widgets by type.
    * `?finish=1`: Filter widgets by finish.
* `/api/v1/widgets/1/`: Returns a specific widget and allows modifications to that widget.
* `/api/v1/widgets/types/`: Returns a list of all the widget types.
* `/api/v1/widgets/sizes/`: Returns a list of all the widget sizes.
* `/api/v1/widgets/finishes/`: Returns a list of all the widget finishes.
* `/api/v1/orders/`: Returns a list of current orders and allows posting of new orders.
* `/api/v1/orders/1/`: Returns a specific order and allows modifications of current orders.
* `/api/v1/orders/1/widgets/`: Returns a the list of widgets associated with an order and allows adding of new widgets.
* `/api/v1/orders/1/widgets/3/`: Returns a widget associated with an order and allows modifications to that widget.

## Improvements

* Separate views and transactions by object type. Currently all transactions are grouped together and all views are grouped together, but as the app grows it would be more logical to group them by their associated objects they are showing or manipulating. It would make adding more objects as the application grows a bit simpler. That would currently be a bit overkill due to the small amount of views and transactions.
* Adding a data model layer. I currently pass around data between views and objects via tuples and dictionaries, but it would help developer understanding if data from each were placed in class instances that can be documented. At the current stage of this application, it would be a bit overkill and take more time.
