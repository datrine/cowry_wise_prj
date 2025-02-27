
from datetime import datetime 
from admin_backend_service.db import get_db
from admin_backend_service.repository.util import (format_user_book_load_row, validate_user_filters)

def save_user_book_loan(book_id:str,user_id:str,return_date:datetime):
    assert book_id is not None
    assert type(book_id) is int
    assert user_id is not None
    assert type(user_id) is int
    assert return_date is not None
    assert isinstance(return_date,datetime)

    db=get_db()
    loan_date=datetime.now()
    params=(book_id,user_id,loan_date.isoformat(),return_date.isoformat())
    res = db.execute("INSERT INTO user_book_loans (book_id,user_id,loan_date,return_date) VALUES(?,?,?,?)",params)
    id = res.lastrowid
    user = {
        "id": id,
        "book_id":book_id,
        "user_id": user_id,
        "loan_date": loan_date,
        "return_date": return_date,
    }
    return user

def get_user_book_loans(filters:dict):
    is_valid=validate_user_filters(filters)
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
                
            res = db.execute("SELECT rowid,book_id,user_id,date(loan_date) as loan_date_dt,date(return_date) as return_date_dt FROM user_book_loans " + where_str, filters)
        else:
            res = db.execute("rowid, book_id,user_id,date(loan_date) as loan_date_dt,date(return_date) as return_date_dt FROM user_book_loans")
        rows = res.fetchall()
        books = []
        for row in rows:
            books.append(format_user_book_load_row(row))
    return books

def get_user_book_loan_by_id(id):
    db=get_db()
    params=(id,)
    res = db.execute("SELECT rowid,book_id,user_id,date(loan_date) as loan_date_dt,date(return_date) as return_date_dt FROM user_book_loans WHERE rowid = ?",params)
    row = res.fetchone()
    if row is None:
        return None
    user = format_user_book_load_row(row)
    return user
    assert email is not None
    assert type(email) is str
    with get_db() as db:
    #db=get_db()
        params=(email,)
        res = db.execute("SELECT rowid, book_id,user_id,loan_date,return_date FROM book_loans WHERE email = ?",params)
        row = res.fetchone()
        if row is None:
            return None
        user = format_user_book_load_row(row=row)
    return user