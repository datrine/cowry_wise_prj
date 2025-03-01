import sqlite3
from app.repository.book import (get_book_by_id,save_book,update_book_by_id,get_books)

def test_save_book(db:sqlite3.Connection):
    assert isinstance(db, sqlite3.Connection)
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

def test_get_book_by_id(existing_book:dict):
    book= dict( get_book_by_id(id=existing_book.get("id")) )
    assert book is not None
    assert book.get("title") == existing_book.get("title")
    assert book.get("category") == existing_book.get("category")
    assert book.get("publisher") == existing_book.get("publisher")

def test_update_book_fields_by_id(existing_book:dict):
    book=  update_book_by_id(id=existing_book.get("id"),update_fields={"category":"new_category","publisher":"new_publisher"})
    assert book is not None
    assert book.get("title") == existing_book.get("title")
    assert book.get("category") == "new_category"
    assert book.get("publisher") == "new_publisher"

def test_get_all_books(db:sqlite3.Connection,existing_book:dict):
    assert isinstance(db, sqlite3.Connection)

    books= get_books(None) 
    assert len(books)  > 0