import sqlite3
from app.repository.borrow_list import (save_borrow_list_item,get_user_book_loan_by_id,get_borrow_list)
from datetime import datetime,timedelta
from faker import Faker
fake=Faker()
def test_save_borrow_list_item(app_context,existing_user,existing_book):
    return_date=datetime.now()+ timedelta(days=fake.random_int(min=1, max=30))
    with app_context:
        book= dict( save_borrow_list_item({
            "user_id":existing_user["id"],
            "book_id":existing_book["id"],
            "email":existing_user["email"],
            "lastname":existing_user["lastname"],
            "firstname":existing_user["firstname"],
            "title":existing_book["title"],
            "category":existing_book["category"],
            "publisher":existing_book["publisher"],
            "loan_date":"2024-01-01",
            "return_date":return_date
        }))
        assert book is not None
        assert book.get("id") is not None
        assert type(book.get("id")) is int 
        assert book.get("title") ==existing_book["title"] 
        assert book.get("lastname") ==existing_user["lastname"]
        assert book.get("firstname") ==existing_user["firstname"]
        assert book.get("category") ==existing_book["category"] 
        assert book.get("publisher") ==existing_book["publisher"]


def test_save_borrow_list_item_no_user_id_error(app_context,existing_user,existing_book):
    return_date=datetime.now()+ timedelta(days=fake.random_int(min=1, max=30))
    with app_context:
        try:
            book= dict( save_borrow_list_item({
                "user_id":None,
                "book_id":existing_book["id"],
                "email":existing_user["email"],
                "lastname":existing_user["lastname"],
                "firstname":existing_user["firstname"],
                "title":existing_book["title"],
                "category":existing_book["category"],
                "publisher":existing_book["publisher"],
                "loan_date":"2024-01-01",
                "return_date":return_date
            }))
            assert False, "Should throw exception"
        except Exception as e:
            assert isinstance(e,AssertionError)

def existing_borrow_list_item_by_id(app_context,existing_borrow_list_item:dict):
    with app_context:
        book= dict( get_user_book_loan_by_id(id=existing_borrow_list_item.get("id")) )
        assert book is not None
        assert book.get("title") == existing_borrow_list_item.get("title")
        assert book.get("category") == existing_borrow_list_item.get("category")
        assert book.get("publisher") == existing_borrow_list_item.get("publisher")


def test_get_all_borrow_list_items(app_context):
    with app_context:
        books= get_borrow_list(None)
        assert len(books)  > 0