from app.blueprints.bp_books import get_book_by_id_handler ,get_books_handler,borrow_book_handler
from flask import Flask
import faker
fake=faker.Faker()
def test_get_books_handler(app:Flask):
    with app.test_request_context():
        [res,status]=get_books_handler()
        assert status==200
        res_data=res.get_json()
        assert res_data.get("data") is not None
        res_data_data=res_data.get("data")
        assert res_data_data is not None



def test_get_book_by_id_handler(app:Flask,existing_book):
    book_id=existing_book.get("id")
    with app.test_request_context():
        [res,status]=get_book_by_id_handler(id=book_id)
        print(res)
        assert status==200
        res_data=res.get_json()
        assert res_data.get("data") is not None
        res_data_data=res_data.get("data")
        assert res_data_data is not None

def test_get_book_by_id_handler_id_missing_error(app:Flask):
    book_id=None
    with app.test_request_context():
        [res,status]=get_book_by_id_handler(id=book_id)
        print(res)
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None

def test_get_book_by_id_handler_not_found_error(app:Flask):
    book_id=fake.random_int(max=100000,min=10000)
    with app.test_request_context():
        [res,status]=get_book_by_id_handler(id=book_id)
        print(res)
        assert status==404
        res_data=res.get_json()
        assert res_data.get("data") is None


def test_borrow_book_handler(app:Flask,existing_book,existing_user):
    data={
        "user_id":existing_user["id"],
        "borrow_days":fake.random_int(min=3, max=10)
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler(id=existing_book["id"])
        assert status==201
        res_data=res.get_json()
        assert res_data.get("data") is not None
        res_data_data=res_data.get("data")
        assert res_data_data.get("email") is not None
        assert res_data_data.get("id") is not None
        assert res_data_data.get("firstname") is not None
        assert res_data_data.get("lastname") is not None
        assert res_data_data.get("return_date") is not None
        assert res_data_data.get("loan_date") is not None
        assert res_data_data.get("email") == existing_user.get("email")
        assert res_data_data.get("firstname") == existing_user.get("firstname")
        assert res_data_data.get("lastname") == existing_user.get("lastname")
        assert res_data_data.get("title") == existing_book.get("title")
        assert res_data_data.get("category") == existing_book.get("category")
        assert res_data_data.get("publisher") == existing_book.get("publisher")


def test_borrow_book_handler_non_existing_book_error(app:Flask,existing_user):
    data={
        "user_id":existing_user["id"],
        "borrow_days":fake.random_int(min=1,max=100),
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler(id=fake.random_int(min=10000, max=100000))
        assert status==404
        res_data=res.get_json()
        assert res_data.get("data") is None

def test_borrow_book_handler_non_existing_user_error(app:Flask,existing_book):
    data={
        "user_id":fake.random_int(min=10000,max=100000),
        "borrow_days":fake.random_int(min=1,max=100),
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler(id=existing_book["id"])
        assert status==404
        res_data=res.get_json()
        assert res_data.get("data") is None

def test_borrow_book_handler_no_user_id_error(app:Flask,existing_book):
    data={
        "user_id":None,
        "book_id":existing_book["id"],
        "borrow_days":fake.random_int(min=1,max=100),
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler(id=existing_book["id"])
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None

def test_borrow_book_handler_no_book_id_error(app:Flask,existing_user):
    data={
        "user_id":existing_user["id"],
        "borrow_days":fake.random_int(min=1,max=100),
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler(id=None)
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None

def test_borrow_book_handler_no_borrow_days_error(app:Flask,existing_book,existing_user):
    data={
        "user_id":existing_book["id"],
        "user_id":existing_user["id"],
        "borrow_days":None
    }
    with app.test_request_context(json=data):
        [res,status]=borrow_book_handler(id=existing_book["id"])
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None
