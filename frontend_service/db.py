import sqlite3
from datetime import datetime
from flask import Flask

import click
from flask import current_app, g

def init_app(app:Flask):
    app.teardown_appcontext(close_db)
    #app.cli.add_command(init_db_command)

def init_db():

    #with current_app.app_context() as ctx:
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def get_db()-> sqlite3.Connection:
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE_URL'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
        db=g.db
    return db

@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

sqlite3.register_converter('timestamp',lambda x: datetime.fromisoformat(x))

sqlite3.register_converter('date',lambda x: datetime.fromisoformat(x))