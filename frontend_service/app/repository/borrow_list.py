
from datetime import datetime 
from app.db import get_db
from app.repository.util import (format_user_book_load_row, validate_user_filters)

def save_user_book_loan(input:dict):
    book_id=input.get('book_id')
    user_id=input.get('user_id')
    email=input.get('email')
    firstname=input.get('firstname')
    lastname=input.get('lastname')
    title=input.get('title')
    category=input.get('category')
    publisher=input.get('publisher')
    return_date=input.get('return_date')
    try:
        assert book_id is not None
        assert user_id is not None
        assert return_date is not None
        assert isinstance(return_date,datetime)
    except AssertionError as e:
        raise(e)
    print("saving user_book_loan")
    with get_db() as db:
        loan_date=datetime.now()
        params=(
                book_id,
                user_id,
                email,
                firstname,
                lastname,
                title,
                category,
                publisher,
                loan_date.isoformat(),
                return_date.isoformat()
            )
        res = db.execute("""
                         INSERT INTO borrow_list 
                         (book_id,user_id,email,firstname,lastname,title,category,publisher,loan_date,return_date) 
                         VALUES(?,?,?,?,?,?,?,?,?,?)
                         """,params)
        id = res.lastrowid
        user = {
            "id": id,
            "book_id":book_id,
            "user_id": user_id,
            "email":email,
            "firstname":firstname,
            "lastname":lastname,
            "title":title,
            "category":category,
            "publisher":publisher,
            "loan_date": loan_date,
            "return_date": return_date,
        }
    return user

def get_borrow_list(filters:dict):
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
                
            res = db.execute("""
                                SELECT rowid,book_id,user_id,book_id,user_id,email,
                                firstname,lastname,title,category,publisher,
                                date(loan_date) as loan_date_dt,date(return_date) as return_date_dt 
                                FROM borrow_list 
                             """ + where_str, filters)
        else:
            res = db.execute("""
                                SELECT rowid, book_id,user_id,book_id,user_id,email,firstname,lastname,
                                title,category,publisher,date(loan_date) as loan_date_dt,
                                date(return_date) as return_date_dt FROM borrow_list
                             """)
        rows = res.fetchall()
        books = []
        for row in rows:
            books.append(format_user_book_load_row(row))
    return books

def get_user_book_loan_by_id(id):
    with get_db() as db:
        params=(id,)
        print(params)
        res = db.execute("""
                            SELECT 
                            rowid, book_id,user_id,book_id,user_id,email,firstname,lastname,
                            title,category,publisher,date(loan_date) as loan_date_dt,
                            date(return_date) as return_date_dt 
                            FROM borrow_list WHERE rowid =?
                        """,params)
        row = res.fetchone()
        if row is None:
            return None
        user = format_user_book_load_row(row)

    return user