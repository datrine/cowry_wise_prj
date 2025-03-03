import os
import tempfile
import sqlite3
from flask import (Flask,Config)
from flask.ctx import (AppContext)
from flask.testing import (FlaskCliRunner)
from datetime import datetime
from faker import Faker
fake = Faker()

import pytest
import logging
logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

from app.db import init_db,get_db
import app.messaging as messaging

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

@pytest.fixture
def app():
    #db_fd, db_path = tempfile.mkstemp()
    app= Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE_URL=os.getenv('DATABASE_URL')if os.getenv('DATABASE_URL')  else "test_db.sqlite",
        RABBITMQ_SERVER=os.getenv('RABBITMQ_SERVER') if os.getenv('RABBITMQ_SERVER') else "localhost",
        RABBITMQ_PORT=os.getenv('RABBITMQ_PORT') if os.getenv('RABBITMQ_PORT') else 5672,
        RABBITMQ_USER=os.getenv('RABBITMQ_USER') if os.getenv('RABBITMQ_USER') else "guest",
        RABBITMQ_PASS=os.getenv('RABBITMQ_PASS') if os.getenv('RABBITMQ_PASS') else "guest",
        RABBITMQ_VHOST=os.getenv('RABBITMQ_VHOST') if os.getenv('RABBITMQ_VHOST') else "/"
    )

    with app.app_context():
        init_db(schema=os.path.join(os.getcwd(),"app", "schema.sql") )
        #get_db().executescript(_data_sql)
        messaging.init()
        #t1=threading.Thread(target=consume_handlers.consume,args=(app,),daemon=True)
        #try:
            #t1.start()
        #except KeyboardInterrupt:
        
    yield app
    
    #app.teardown_request()
    # clean up the temporary db
    #os.close(db_fd)
    #if os.path.exists("test_db.sqlite"):
        #os.unlink("test_db.sqlite")
    with app.app_context():
        from .utils import cleanup_rmq 
        cleanup_rmq()


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
def existing_user(db:sqlite3.Connection)->dict:
    with db:
        params=(fake.email(),fake.first_name(),fake.last_name(),"USER")
        id= db.execute("""
                       INSERT INTO users (email, firstname, lastname,role) 
                       VALUES (?,?,?,?)
                       """,params).lastrowid
        select_params=(id,)
        cursor= db.execute("""
                           SELECT rowid,email, firstname, lastname
                           FROM users where rowid=?
                           """,select_params)
        row=cursor.fetchone()
        mylogger.info ({"id":id,"par":select_params,"row":row})
        book = {
                "id": row["rowid"],
                "email":row["email"],
                "firstname": row["firstname"],
                "lastname": row["lastname"],
            }
    return book

@pytest.fixture
def existing_book(db:sqlite3.Connection)->dict:
    with db:
        params=("existing_title","existing_publisher","existing_category",1)
        id= db.execute("""
                       INSERT INTO books (title, publisher, category, is_available) 
                       VALUES (?,?,?,?)
                       """,params).lastrowid
        select_params=(id,)
        cursor= db.execute("""
                           SELECT rowid, title, publisher, category, is_available 
                           FROM books where rowid=?""",select_params)
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
def existing_borrow_list_item(db:sqlite3.Connection)->dict:
    with db:
        book_id=1
        user_id=12
        loan_date=datetime.now()
        return_date=datetime.now()
        params=(book_id,user_id,loan_date.isoformat(), return_date.isoformat())
        id= db.execute("INSERT INTO user_book_loans (book_id,user_id,loan_date, return_date) VALUES(?,?,?,?)",params).lastrowid
        select_params=(id,)
        cursor= db.execute("""
                           SELECT rowid,book_id,user_id,date(loan_date) as loan_date_dt, 
                           date(return_date) as return_date_dt FROM user_book_loans 
                           WHERE rowid = ?""",select_params)
        row=cursor.fetchone()
        mylogger.info ({"id":id,"par":select_params,"row":row})
        user_book_loan = {
                "id": row["rowid"],
                "book_id":row["book_id"],
                "user_id": row["user_id"],
                "loan_date": row["loan_date_dt"],
                "return_date":row["return_date_dt"],
            }
    return user_book_loan