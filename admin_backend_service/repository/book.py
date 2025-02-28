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
        res = db.execute("""
                         SELECT rowid,title,publisher,category, is_available,
                         date(loan_date) as loan_date_dt,
                         date(return_date) as return_date_dt FROM books WHERE rowid = ?""",params)
        row = res.fetchone()
        if row is None:
            return None
    book = format_book_row(row=row)
    return book

def delete_book_by_id(id):
    with get_db() as db:
        params=(id,)
        res = db.execute("DELETE  FROM books WHERE rowid = ?",params)
        if res.rowcount != 1:
            return None
    return id

def get_books(filters:dict):
    is_valid=validate_book_filters(filters)
    if is_valid is not True:
        raise Exception("Invalid filters")
    with get_db() as db:
        where_str= ""
        prev=False
        params=tuple()
        if filters is not None:
            for filter in filters:
                print({filter:filters.get(filter)})
                if filters.get(filter) is None:
                    continue
                if where_str == "":
                    where_str += " WHERE "
                if prev:
                    where_str += " AND "
                where_str += f"{filter} = ? "
                if filter == "is_available":
                    params+=(1 if bool(filters.get(filter))  else 0,)
                else:
                    params += (filters.get(filter),)
                prev = True
            sql="""
                SELECT rowid,title,publisher,category,is_available,date(loan_date) as loan_date_dt,
                date(return_date) as return_date_dt FROM books 
                """ + where_str
            print(filters,params, sql)   
            res = db.execute(sql, params)
        else:
            sql="""
                SELECT rowid,title, publisher, category, is_available,date(loan_date) as loan_date_dt,
                            date(return_date) as return_date_dt FROM books
            """
            print(sql)   
            res = db.execute(sql)
        rows = res.fetchall()
        books = []
        for row in rows:
            books.append(format_book_row(row=row))
    return books

def update_book_by_id(id,update_fields:dict):
    assert id is not None
    print("id",id)
    #assert type(id) is int
    validate_book_updatable_fields(update_fields)
    with get_db() as db:
        params=tuple()
        set_str= ""
        prev=False
        for field in update_fields:
            if set_str == "":
                set_str += "SET "
            if prev:
                set_str += ", "
            set_str += f"{field} = ? "
            if field == "is_available":
                params+=(1 if bool(update_fields.get(field))  else 0,)
            else: params += (update_fields[field],)
            prev = True
        params =params+ (id,)
        sql="UPDATE books "+set_str+ " WHERE rowid=?"
        res = db.execute(sql,params)
        if res.rowcount == 0:
            raise Exception("Update failed for book id "+id)
        res = db.execute("""
                         SELECT rowid,title,publisher,category, is_available,date(loan_date) as loan_date_dt,
                            date(return_date) as return_date_dt from books WHERE rowid=?
                         """,(id,))
        row = res.fetchone()
        book = format_book_row(row=row)
    return book