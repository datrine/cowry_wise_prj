import sqlite3 
from admin_backend_service.repository.util import (validate_book_filters,validate_book_updatable_fields,format_book_row)
from admin_backend_service.db import get_db

def save_book(title:str,publisher:str,category:str):
    assert title is not None
    assert type(title) is str
    assert publisher is not None
    assert type(publisher) is str
    assert category is not None
    assert type(category) is str

    with get_db() as db:
        is_available=True
        params=(title,publisher,category,is_available)
        res = db.execute("INSERT INTO books (title,publisher,category,is_available) VALUES(?,?,?,?)",params)
        id = res.lastrowid
        book = {
            "id": id,
            "title":title,
            "publisher": publisher,
            "category": category,
            "is_available":is_available,
        }
    return book

def get_book_by_id(id):
    with get_db() as db:
        params=(id,)
        res = db.execute("SELECT rowid,title,publisher,category, is_available FROM books WHERE rowid = ?",params)
        row = res.fetchone()
        if row is None:
            return None
    book = format_book_row(row=row)
    return book

def get_books(filters:dict):
    is_valid=validate_book_filters(filters)
    if is_valid is not True:
        raise Exception("Invalid filters")
    with get_db() as db:
        where_str= ""
        prev=False
        if filters is not None:
            for filter in filters:
                if where_str != "":
                    where_str += " WHERE "
                if prev:
                    where_str += " AND "
                where_str += f"{filter} = ? "
                prev = True
                
            res = db.execute("SELECT rowid,title,publisher,category,is_available FROM books " + where_str, filters)
        else:
            res = db.execute("SELECT rowid,title,publisher,category,is_available FROM books ")
        rows = res.fetchall()
        books = []
        for row in rows:
            books.append(format_book_row(row=row))
    return books

def update_book_by_id(id,update_fields:dict):
    assert id is not None
    assert type(id) is int
    validate_book_updatable_fields(update_fields)
    with get_db() as db:
        params=tuple()
        set_str= ""
        prev=False
        for filter in update_fields:
            if set_str == "":
                set_str += "SET "
            if prev:
                set_str += ", "
            set_str += f"{filter} = ? "
            params += (update_fields[filter],)
            prev = True
        params =params+ (id,)
        sql="UPDATE books "+set_str+ " WHERE rowid=?"
        print(sql)
        res = db.execute(sql,params)
        if res.rowcount == 0:
            raise Exception("Update failed for book id "+id)
        res = db.execute("SELECT rowid,title,publisher,category, is_available from books WHERE rowid=?",(id,))
        row = res.fetchone()
        book = format_book_row(row=row)
    return book