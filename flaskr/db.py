"""
The first thing to do when working with a SQLite database
(and most other database libraries in Python) is to create
a connection to the database.

Any queries and operations are performed using the connection
and it is closed after the work is finished.

In web apps, the connection is typically tied to the request.
It is created at some point when handling a request, and 
closed before the response is sent.
"""

import sqlite3
import click
from flask import current_app, g

def get_db():
    """
    This function gets an existing database connection if available
    and creates one if one is not available.
    """
    if 'db' not in g:
        """
        g is a special flask object that is unique for each request. It is used to store data 
        that may be accessed by multiple functions during the request.
        The connection is stored and reused instead of creating a new connection if get_db
        is called a second time in that same request.

        so this if statement checks that a connection is not already stored in g. If one is
        not present, it creates a brand new connection.

        -------------------------------------------------------------------------------------

        current_app is another special flask object that points to the Flask app handling
        the request.
        Since an app factory is being used to handle creating the app, there is no app object
        when writing the rest of your code. so get_db will be called when the app has been
        created and is handling a request, so current_app can be used.
        """
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row # tells the connection to return rows that behave like dicts

        return g.db
    

def close_db(e=None):
    """
    This function checks if a connection was created by checking if g.db was set.
    If the connection exists, it is closed.

    This function will be called in the app factory after each request, so that the connection
    to the db is closed.
    """
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """
    This function creates the database tables from the schema.sql file.
    """
    db = get_db() # gets an existing db connection or creates one

    # open_resource opens a file relative to the flaskr package, which is useful since you
    # won't always know where the location is when deploying the app later
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8')) # executes the SQL commands in the script


@click.command('init-db') # defines a CLI command that calls the init_db function
def init_db_command():
    """Clear the existing data and creates new tables."""
    init_db()
    click.echo('Initialized the database')


def init_app(app):
    """
    This function tells flask to close the db when cleaning up after returning the response
    (app.teardown_appcontext), and adds a new command that can be called with the flask command
    (app.cli.add_command).

    This function will be called in the app factory in __init__.py.
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)