import sqlite3
from datetime import datetime
from app.repository.borrow_list import (save_user_book_loan,get_user_book_loan_by_id,get_borrow_list)
from faker import Faker
fake = Faker()

def test_save_borrow(db:sqlite3.Connection):
    assert isinstance(db, sqlite3.Connection)
    book_id=12
    user_id=2
    email=fake.email()
    lastname=fake.last_name()
    firstname=fake.first_name()
    book_title=fake.sentence()
    book_category=fake.word()
    publisher=fake.company()
    return_date=datetime.fromisoformat(f'2026-02-02')
    user_book_loan=  save_user_book_loan({
        "book_id":book_id,
        "user_id":user_id,
        "email":email,
        "lastname":lastname,
        "firstname":firstname,
        "title":book_title,
        "category":book_category,
        "publisher":publisher,
        "return_date":return_date
        })
    assert user_book_loan is not None
    assert user_book_loan.get("id") is not None
    assert type(user_book_loan.get("id")) is int 
    assert user_book_loan.get("book_id") == book_id
    assert user_book_loan.get("return_date") == return_date
    assert user_book_loan.get("user_id") ==user_id

def test_get_borrow_by_id(existing_user_book_loan:dict):
    print(existing_user_book_loan)
    user_book_loan= dict( get_user_book_loan_by_id(id=existing_user_book_loan.get("id")))
    assert user_book_loan is not None
    assert user_book_loan.get("id") is not None
    assert type(user_book_loan.get("id")) is int 
    assert user_book_loan.get("book_id") == existing_user_book_loan.get("book_id")
    assert user_book_loan.get("return_date") ==existing_user_book_loan.get ("return_date")
    assert user_book_loan.get("user_id") ==existing_user_book_loan.get ("user_id")