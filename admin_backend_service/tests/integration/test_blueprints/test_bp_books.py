from app.blueprints.bp_books import get_book_by_id_handler ,get_books_handler
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



#def test_get_book_by_id_handler_any_server_error(app:Flask,existing_book):
#    book_id=existing_book.get("id")
#    #with app.test_request_context():
#    [res,status]=get_book_by_id_handler(id=book_id)
#    print(res)
#    assert status==500
#    res_data=res.get_json()
#    assert res_data.get("data") is None