import os
import tempfile
import sqlite3
from flask import (Flask,Config)
from flask.ctx import (AppContext)
from flask.testing import (FlaskCliRunner)
from datetime import datetime

import pytest
import logging
from faker import Faker
fake = Faker()
logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

from app import create_app
from app.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING': True,
        'DATABASE_URL': db_path
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)
    
    yield app

    # clean up the temporary db
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app:Flask):
    return app.test_client()

@pytest.fixture
def runner(app:Flask)-> FlaskCliRunner:
    return app.test_cli_runner()

@pytest.fixture
def app_context(app:Flask):
    with app.app_context() as ctx:
        yield ctx

@pytest.fixture
def app_context_with_db(app:Flask, app_context:AppContext):
    app_context.g.db= sqlite3.connect(
            app.config['DATABASE_URL'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
    app_context.g.db.row_factory = sqlite3.Row
    yield app_context


@pytest.fixture
def db(app_context_with_db:AppContext)->sqlite3.Connection:
    db= app_context_with_db.g.get("db")
    return db


@pytest.fixture
def existing_book(db:sqlite3.Connection)->dict:
    with db:
        params=("existing_title","existing_publisher","existing_category",1)
        id= db.execute("INSERT INTO books (title, publisher, category, is_available) VALUES (?,?,?,?)",params).lastrowid
        select_params=(id,)
        cursor= db.execute("SELECT rowid, title, publisher, category, is_available FROM books where rowid=?",select_params)
        row=cursor.fetchone()
        mylogger.info ({"id":id,"par":select_params,"row":row})
        book = {
                "id": row["rowid"],
                "title":row["title"],
                "publisher": row["publisher"],
                "category": row["category"],
                "is_available":row["is_available"],
            }
    return book

@pytest.fixture
def existing_user_book_loan(db:sqlite3.Connection)->dict:
    with db:
        book_id=1
        user_id=12
        email=fake.email()
        lastname=fake.last_name()
        firstname=fake.first_name()
        book_title=fake.sentence()
        book_category=fake.word()
        publisher=fake.company()
        loan_date=datetime.now()
        return_date=datetime.now()
        params=(
            book_id,user_id,email,lastname,firstname,
            book_title,book_category,publisher, 
            loan_date.isoformat(), return_date.isoformat())
        id= db.execute("""
                       INSERT INTO borrow_list 
                       (book_id,user_id,email,lastname,firstname,title,category,publisher,loan_date, 
                       return_date) VALUES(?,?,?,?,?,?,?,?,?,?)
                       """,params).lastrowid
        select_params=(id,)
        cursor= db.execute("""
                           SELECT 
                           rowid,book_id,user_id,email,lastname,firstname,title,category,publisher,
                           date(loan_date) as loan_date_dt, date(return_date) as return_date_dt 
                           FROM borrow_list WHERE rowid = ?
                           """,select_params)
        row=cursor.fetchone()
        mylogger.info ({"id":id,"par":select_params,"row":row})
        user_book_loan = {
                "id": row["rowid"],
                "book_id":row["book_id"],
                "user_id": row["user_id"],
                "email": row["email"],
                "lastname": row["lastname"],
                "firstname": row["firstname"],
                "title": row["title"],
                "category": row["category"],
                "publisher": row["publisher"],
                "loan_date": row["loan_date_dt"],
                "return_date":row["return_date_dt"],
            }
    return user_book_loan