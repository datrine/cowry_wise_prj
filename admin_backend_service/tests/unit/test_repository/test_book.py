import faker
from app.repository.book import (get_book_by_id,save_book,update_book_by_id,get_books)
fake= faker.Faker()
def test_save_book(db_execute_save_user):
    with db_execute_save_user:
        title="title"
        publisher="publisher"
        category="white"
        book= dict( save_book(title=title,publisher=publisher,category=category))
        assert book is not None
        assert book.get("id") is not None
        assert type(book.get("id")) is int 
        assert book.get("title") == title
        assert book.get("category") == category
        assert book.get("publisher") ==publisher


def test_save_book_no_title_raises_error(db_execute_save_user):
    with db_execute_save_user:
        title=None
        publisher="publisher"
        category="white"
        try:
            book= dict(save_book(title=title, publisher=publisher, category=category))
            assert False, "should throw exception that title is missing"
        except Exception as e:
            assert e is not None
            isinstance(e,AssertionError)


def test_save_book_no_catgeory_raises_error(db_execute_save_user):
    with db_execute_save_user:
        title=fake.word()
        publisher="publisher"
        category=None
        try:
            book= dict(save_book(title=title, publisher=publisher, category=category))
            assert False, "should throw exception that category is missing"
        except Exception as e:
            assert e is not None
            isinstance(e,AssertionError)
def test_save_book_no_publisher_raises_error(db_execute_save_user):
    with db_execute_save_user:
        title=fake.word()
        publisher=None
        category=fake.word()
        try:
            book= dict(save_book(title=title, publisher=publisher, category=category))
            assert False, "should throw exception that publisher is missing"
        except Exception as e:
            assert e is not None
            isinstance(e,AssertionError)
def test_get_book_by_id(existing_book,db_execute_get_user_by_id):
    with db_execute_get_user_by_id:
        book= dict( get_book_by_id(id=existing_book.get("id")) )
        assert book is not None
        assert book.get("title") == existing_book.get("title")
        assert book.get("category") == existing_book.get("category")
        assert book.get("publisher") == existing_book.get("publisher")

def test_return_null_for_non_existing_book(db_execute_get_non_existing_book):
    with db_execute_get_non_existing_book:
        book= dict( get_book_by_id(id=fake.random_int(min=1,max=5)) )
        assert book is None

def test_update_book_fields_by_id(db_execute_update_book_by_id,existing_book:dict):
    with db_execute_update_book_by_id:
        book=  update_book_by_id(id=existing_book.get("id"),update_fields={
            "category":"new_category","publisher":"new_publisher"})
        assert book is not None

def test_get_all_books(db_execute_get_all_books):
    with db_execute_get_all_books:
        books= get_books(None) 
        assert len(books)  > 0

"""
"""