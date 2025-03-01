import sqlite3
from app.repository.user import (get_user_by_email,save_user)

def test_save_user(db:sqlite3.Connection):
    assert isinstance(db, sqlite3.Connection)
    email="test2test.co"
    lastname="betty"
    firstname="white"
    user= save_user(email=email,lastname=lastname,firstname=firstname)
    assert user is not None
    assert user.get("id") is not None
    assert type(user.get("id")) is int 
    assert user.get("email") == email
    assert user.get("firstname") == firstname
    assert user.get("lastname") ==lastname

def test_get_user_by_email(db:sqlite3.Connection):
    assert isinstance(db, sqlite3.Connection)
    user= dict( get_user_by_email(email='test@test.co'))
    assert user is not None
    assert user.get("email") == 'test@test.co'
    assert user.get("firstname") == 'joe'
    assert user.get("lastname") == 'doe'