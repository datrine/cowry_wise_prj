from app.blueprints.bp_borrow_list import  list_of_users_and_books_borrowed_handler
from flask import Flask
import faker
from datetime import datetime
from datetime import timedelta
fake=faker.Faker()
def test_list_of_users_and_books_borrowed_handler(app:Flask):
    with app.test_request_context():
        [res,status]=list_of_users_and_books_borrowed_handler()
        assert status==200
        res_data=res.get_json()
        assert res_data.get("data") is not None
