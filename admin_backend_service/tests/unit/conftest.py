import os
import tempfile
import sqlite3
from flask import (Flask,Config)
from flask.ctx import (AppContext)
from flask.testing import (FlaskCliRunner)
from datetime import datetime,timedelta
from faker import Faker
fake = Faker()

import pytest
import logging
logging.basicConfig(level=logging.DEBUG)
mylogger = logging.getLogger()

@pytest.fixture
def app():
    #db_fd, db_path = tempfile.mkstemp()
    app= Flask(__name__, instance_relative_config=True)
    return app


@pytest.fixture
def client(app:Flask):
    return app.test_client()

@pytest.fixture
def runner(app:Flask)-> FlaskCliRunner:
    return app.test_cli_runner()

@pytest.fixture
def app_context(app:Flask,monkeypatch):
    #monkeypatch.setattr(app,"app_context",lambda: dict())
    return app.app_context()

@pytest.fixture
def app_context_with_db( app_context:AppContext,monkeypatch):
    from .db import DBConnectionMock
    mock_db=DBConnectionMock()
    app_context.g.db=mock_db
    #monkeypatch.setattr(app_context.g, "db", mock_db, raising=True)
    yield app_context


@pytest.fixture
def db(app_context_with_db:AppContext)->sqlite3.Connection:
    db= app_context_with_db.g.get("db")
    return db

@pytest.fixture
def db_execute_save_user(db:sqlite3.Connection):
     fetchone=lambda email,lastname,firstname:dict({
         "email":email,
         "lastname":lastname,
         "firstname":firstname})
     execute=lambda str:fetchone
     db.execute=execute
     return db

@pytest.fixture
def db_execute_get_user_by_id(db:sqlite3.Connection):
     fetchone=lambda id:dict({
         "id":id,
         "email":fake.email(),"lastname":fake.last_name(),"firstname":fake.first_name()})
     execute=lambda str:fetchone
     db.execute=execute
     return db

@pytest.fixture
def db_execute_get_non_existing_book(db:sqlite3.Connection):
     fetchone=lambda :None
     execute=lambda str:fetchone
     db.execute=execute
     return db
@pytest.fixture
def db_execute_update_book_by_id(db:sqlite3.Connection):
    def execute(sql:str,params:tuple):
        if sql.startswith("UPDATE"):
            category,publisher,id=params
            return {"rowcount":1}
        elif sql.startswith("SELECT"):
            
            fetchone=lambda: dict({
                            "id":id,
                            "title":fake.word(),
                            "publisher":fake.word(),
                            "category":fake.word(),
                            "is_available":True})
            return fetchone
    db.execute=execute
    return db

@pytest.fixture
def db_execute_get_all_books(db:sqlite3.Connection):
    def execute(sql:str,params:tuple):
        def fetchone(): 
            list_of_books=[]
            for id in range(1,10):
                list_of_books.append(dict({
                    "id":id,
                    "title":fake.word(),
                    "publisher":fake.word(),
                    "category":fake.word(),
                    "is_available":True}))
            return list_of_books
        return fetchone
    db.execute=execute
    return db

@pytest.fixture
def existing_user(db:sqlite3.Connection)->dict:
    with db:
        book = {
                "email": fake.email(),
                "id":1,
                "firstname":fake.first_name(),
                "lastname": fake.last_name(),
                "role":"USER"
            }
    return book

@pytest.fixture
def existing_book()->dict:
    book = {
            "id": 1,
            "title":fake.word(),
            "publisher": fake.company(),
            "category": fake.sentence(),
            "is_available":True,
        }
    return book

@pytest.fixture
def existing_borrow_list_item(db:sqlite3.Connection)->dict:
    user_book_loan = {
            "id": 1,
            "book_id":1,
            "user_id": 1,
            "loan_date": datetime.now(),
            "return_date":datetime.now()+timedelta(days=10),
        }
    return user_book_loan