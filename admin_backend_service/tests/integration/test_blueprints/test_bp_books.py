from app.blueprints.bp_books import( 
    get_book_by_id_handler ,
    get_books_handler,add_book_handler,
    get_unavailable_books_handler,update_book_handler,delete_book_handler)
from flask import Flask
import faker
fake=faker.Faker()

def test_add_book_handler(app:Flask):
    data={
        "title":fake.word(),
        "category":fake.word(),
        "publisher":fake.word(),
    }
    with app.test_request_context(json=data):
        [res,status]=add_book_handler()
        print(res)
        assert status==201
        res_data=res.get_json()
        assert res_data.get("data") is not None
        assert res_data.get("data").get("id") is not None
        assert res_data.get("data").get("title") is not None
        assert res_data.get("data").get("title") == data.get("title")
        assert res_data.get("data").get("category") is not None
        assert res_data.get("data").get("category") == data.get("category")
        assert res_data.get("data").get("publisher") is not None
        assert res_data.get("data").get("publisher") == data.get("publisher")

def test_add_book_handler_no_title_error(app:Flask):
    data={
        "title":None,
        "category":fake.word(),
        "publisher":fake.word(),
    }
    with app.test_request_context(json=data):
        [res,status]=add_book_handler()
        print(res)
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None


def test_add_book_handler_no_category_error(app:Flask):
    data={
        "title":fake.word(),
        "category":None,
        "publisher":fake.word(),
    }
    with app.test_request_context(json=data):
        [res,status]=add_book_handler()
        print(res)
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None


def test_add_book_handler_no_publisher_error(app:Flask):
    data={
        "title":fake.word(),
        "category":fake.word(),
        "publisher":None,
    }
    with app.test_request_context(json=data):
        [res,status]=add_book_handler()
        print(res)
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None


def test_get_books_handler(app:Flask):
    with app.test_request_context():
        [res,status]=get_books_handler()
        assert status==200
        res_data=res.get_json()
        assert res_data.get("data") is not None
        res_data_data=res_data.get("data")
        assert res_data_data is not None


def test_get_unavailable_books_handler(app:Flask,existing_unavailable_book):
    with app.test_request_context():
        [res,status]=get_unavailable_books_handler()
        #assert status==200
        res_data=res.get_json()
        print(res_data)
        assert res_data.get("data") is not None
        res_data_data=res_data.get("data")
        assert res_data_data is not None
        for book in res_data_data:
            assert book.get("is_available")==False


def test_get_book_by_id_handler(app:Flask,existing_book):
    book_id=existing_book.get("id")
    with app.test_request_context():
        [res,status]=get_book_by_id_handler(id=book_id)
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


def test_delete_book_by_id_handler(app:Flask,existing_book):
    book_id=existing_book.get("id")
    with app.test_request_context():
        [res,status]=delete_book_handler(id=book_id)
        assert status==200

def test_delete_book_by_id_handler_no_id_error(app:Flask,existing_book):
    with app.test_request_context():
        [res,status]=delete_book_handler(id=None)
        assert status==400

def test_delete_book_by_id_handler_non_existing_error(app:Flask):
    with app.test_request_context():
        [res,status]=delete_book_handler(id=fake.random_int(min=10000,max=100000))
        assert status==404

def test_update_book_handler(app:Flask,existing_book):
    data={
        "is_available":False,
        "category":fake.word(),
        "publisher":fake.word(),
    }
    with app.test_request_context(json=data):
        [res,status]=update_book_handler(id=existing_book.get("id"))
        print(res)
        assert status==200
        res_data=res.get_json()
        assert res_data.get("data") is not None
        res_data_data=res_data.get("data")
        assert res_data_data is not None
        assert res_data_data.get("is_available")==data.get("is_available")
        assert res_data_data.get("category")==data.get("category")


def test_update_book_handler_non_existing_book_id_error_response(app:Flask):
    data={
        "is_available":False,
        "category":fake.word(),
        "publisher":fake.word(),
    }
    with app.test_request_context(json=data):
        [res,status]=update_book_handler(id=fake.random_int(max=100000, min=10000))
        print(res)
        assert status==404
        res_data=res.get_json()
        assert res_data.get("data") is None
