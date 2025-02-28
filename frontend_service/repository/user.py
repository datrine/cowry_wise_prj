from frontend_service.db import get_db
from frontend_service.repository.util import (format_user_row,validate_user_filters,validate_user_updatable_fields)

"""
save_user(email:str,firstname:str,lastname:str) -> dict:
save user
"""
def save_user(email:str,firstname:str,lastname:str):
    assert email is not None
    assert type(email) is str
    assert firstname is not None
    assert type(firstname) is str
    assert lastname is not None
    assert type(lastname) is str

    with get_db() as db:
        role="USER"
        params=(email,firstname,lastname,role)
        res = db.execute("INSERT INTO users (email,firstname,lastname,role) VALUES(?,?,?,?)",params)
        id = res.lastrowid
        user = {
            "id": id,
            "email":email,
            "firstname": firstname,
            "lastname": lastname,
            "role": role,
        }
    return user

"""
get_users(filters:dict) -> List[dict]:
get users (filterable)
"""
def get_users(filters:dict):

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
                
            res = db.execute("SELECT rowid, email,firstname,lastname, role FROM users " + where_str, filters)
        else:
            res = db.execute("SELECT rowid, email,firstname,lastname, role FROM users")
        rows = res.fetchall()
        books = []
        for row in rows:
            books.append(format_user_row(row))
    return books


"""
get_users(filters:dict) -> List[dict]:
get users (filterable)
"""
def get_users_by_ids(filters:tuple):

    with get_db() as db:
        where_str= ""
        prev=False
        if  len(filters) > 0:
            where_str += " WHERE "
            for filter in filters:
                if prev:
                    where_str += " OR "
                where_str += f"rowid = ? "
                prev = True
                
            res = db.execute("SELECT rowid, email,firstname,lastname, role FROM users " + where_str, filters)
        else:
            res = db.execute("SELECT rowid, email,firstname,lastname, role FROM users")
        rows = res.fetchall()
        books = []
        for row in rows:
            books.append(format_user_row(row))
    return books





"""
get_user_by_id(id:str) -> dict:
get user by id
"""
def get_user_by_id(id):
    with get_db() as db:
        params=(id,)
        res = db.execute("SELECT rowid,email,firstname,lastname,role FROM users WHERE rowid = ?",params)
        row = res.fetchone()
        if row is None:
            return None
        user = {
            "id": row["rowid"],
            "email": row["email"],
            "firstname": row["firstname"],
            "lastname": row["lastname"],
            "role": row["role"],
        }
        return user

"""
get_user_by_email(email:str) -> dict:
get user by email
"""
def get_user_by_email(email):
    assert email is not None
    assert type(email) is str
    with get_db() as db:
        params=(email,)
        res = db.execute("SELECT rowid, email,firstname,lastname, role FROM users WHERE email = ?",params)
        row = res.fetchone()
        if row is None:
            return None
        user = format_user_row(row=row)
    return user


def update_user_by_id(id,update_fields:dict):
    assert id is not None
    assert type(id) is int
    validate_user_updatable_fields(update_fields)
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
        sql="UPDATE users "+set_str+ " WHERE rowid=?"
        print(sql)
        res = db.execute(sql,params)
        if res.rowcount == 0:
            raise Exception("Update failed for user id "+id)
        res = db.execute("SELECT rowid,email,lastname,firstname,role from books WHERE rowid=?",(id,))
        row = res.fetchone()
        book = format_user_row(row=row)
    return book