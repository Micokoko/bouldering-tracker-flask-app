import sqlite3
import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES
        )
        g.db.row_factory = sqlite3.Row
    return g.db



def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
 
    db.executescript('''
        DROP TABLE IF EXISTS user;
        DROP TABLE IF EXISTS boulder;
        DROP TABLE IF EXISTS attempt
    ''')

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


import sqlite3

def convert_timestamp(val):
    try:

        if isinstance(val, str) and ' ' in val:
            datepart, timepart = val.split(' ')
            return datepart, timepart
        else:

            return val, None
    except ValueError:
        return val, None
