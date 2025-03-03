from app.blueprints.bp_borrow_list import borrow_book_handler ,list_of_users_and_books_borrowed_handler
from flask import Flask
import faker
from datetime import datetime
from datetime import timedelta
fake=faker.Faker()
def test_borrow_book_handler(app:Flask,existing_book,existing_user):
    data={
        "book_id":existing_book["id"],
        "user_id":existing_user["id"],
        "return_date":(datetime.now()+timedelta(days=3)).isoformat()
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler()
        assert status==201
        res_data=res.get_json()
        assert res_data.get("data") is not None
        res_data_data=res_data.get("data")
        assert res_data_data.get("email") is not None
        assert res_data_data.get("id") is not None
        assert res_data_data.get("firstname") is not None
        assert res_data_data.get("lastname") is not None
        assert res_data_data.get("email") == existing_user.get("email")
        assert res_data_data.get("firstname") == existing_user.get("firstname")
        assert res_data_data.get("lastname") == existing_user.get("lastname")
        assert res_data_data.get("title") == existing_book.get("title")
        assert res_data_data.get("category") == existing_book.get("category")
        assert res_data_data.get("publisher") == existing_book.get("publisher")
        d1=datetime.fromisoformat(res_data_data.get("return_date"))
        d2= datetime.fromisoformat( data.get("return_date"))
        assert d1.year == d2.year and d1.month == d2.month and d1.day == d2.day


def test_borrow_book_handler_non_existing_book_error(app:Flask,existing_user):
    data={
        "book_id":fake.random_int(min=10000,max=100000),
        "user_id":existing_user["id"],
        "return_date":(datetime.now()+timedelta(days=3)).isoformat()
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler()
        assert status==404
        res_data=res.get_json()
        assert res_data.get("data") is None

def test_borrow_book_handler_non_existing_user_error(app:Flask,existing_book):
    data={
        "book_id":existing_book["id"],
        "user_id":fake.random_int(min=10000,max=100000),
        "return_date":(datetime.now()+timedelta(days=3)).isoformat()
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler()
        assert status==404
        res_data=res.get_json()
        assert res_data.get("data") is None

def test_borrow_book_handler_no_user_id_error(app:Flask,existing_book):
    data={
        "user_id":None,
        "book_id":existing_book["id"],
        "return_date":(datetime.now()+timedelta(days=3)).isoformat()
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler()
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None

def test_borrow_book_handler_no_book_id_error(app:Flask,existing_user):
    data={
        "user_id":existing_user["id"],
        "book_id":None,
        "return_date":(datetime.now()+timedelta(days=3)).isoformat()
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler()
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None

def test_borrow_book_handler_no_user_id_error(app:Flask,existing_book,existing_user):
    data={
        "user_id":existing_book["id"],
        "user_id":existing_user["id"],
        "return_date":None
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler()
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None

def test_list_of_users_and_books_borrowed_handler(app:Flask):
    with app.test_request_context():
        [res,status]=list_of_users_and_books_borrowed_handler()
        assert status==200
        res_data=res.get_json()
        assert res_data.get("data") is not None
