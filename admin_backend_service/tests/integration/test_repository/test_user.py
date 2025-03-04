import sqlite3
from app.repository.user import (get_user_by_id,save_user,update_user_by_id,get_users)
from faker import Faker
fake=Faker()
def test_save_user(app_context):
    with app_context:
        email=fake.email()
        lastname=fake.last_name()
        firstname=fake.first_name()
        book= dict( save_user(
            email=email,
            lastname=lastname,
            firstname=firstname
        ))
        assert book is not None
        assert book.get("id") is not None
        assert type(book.get("id")) is int 
        assert book.get("email") == email
        assert book.get("firstname") == firstname
        assert book.get("lastname") ==lastname

def test_save_book_no_email_raises_error(db:sqlite3.Connection):
    with db:
        email=None
        lastname=fake.last_name()
        firstname=fake.first_name()
        try:
            book= dict(save_user(
                email=email, 
                lastname=lastname, 
                firstname=firstname))
            assert False, "should throw exception that email is missing"
        except Exception as e:
            assert e is not None
            isinstance(e,AssertionError)

def test_save_book_no_firstname_raises_error(db:sqlite3.Connection):
    with db:
        email=fake.email()
        lastname=None
        firstname=fake.first_name()
        try:
            book= dict(save_user(
                email=email, 
                lastname=lastname, 
                firstname=firstname))
            assert False, "should throw exception that lastname is missing"
        except Exception as e:
            assert e is not None
            isinstance(e,AssertionError)

def test_save_book_no_lastname_raises_error(db:sqlite3.Connection):
    with db:
        email=fake.email()
        lastname=fake.last_name()
        firstname=None
        try:
            book= dict(save_user(
                email=email, 
                lastname=lastname, 
                firstname=firstname))
            assert False, "should throw exception that firstname is missing"
        except Exception as e:
            assert e is not None
            isinstance(e,AssertionError)

def test_get_user_by_id(existing_user:dict):
    book= dict( get_user_by_id(id=existing_user.get("id")) )
    assert book is not None
    assert book.get("email") == existing_user.get("email")
    assert book.get("lastname") == existing_user.get("lastname")
    assert book.get("firstname") == existing_user.get("firstname")

def test_get_user_by_id_non_existing_user(app_context):
    with app_context:
        book= get_user_by_id(id=fake.random_int(min=1000,max=2000)) 
        assert book is None

def test_update_user_fields_by_id(existing_user:dict):
    lastname=fake.last_name()
    firstname=fake.first_name()
    email=fake.email()
    user=  update_user_by_id(id=existing_user.get("id"),update_fields={
        "email":email,
        "lastname":lastname,
        "firstname":firstname
        })
    assert user is not None
    assert user.get("email") == email
    assert user.get("lastname") == lastname
    assert user.get("firstname") == firstname

def test_update_user_fields_by_id_non_exixting_user(app_context):
    with app_context: 
        lastname=fake.last_name()
        firstname=fake.first_name()
        email=fake.email()
        try:
            update_user_by_id(id=fake.random_int(min=10000,max=100000),update_fields={
                "email":email,
                "lastname":lastname,
                "firstname":firstname
                })
            assert False, "should throw exception that user does not exist"
        except Exception as e:
            assert e is not None

def test_update_user_fields_by_id_invaid_update_field(app_context):
    with app_context: 
        try:
            update_user_by_id(id=fake.random_int(min=10000,max=100000),update_fields={
                "invalid_field":"invalid_field_value",
                })
            assert False, "should throw exception that user does not exist"
        except Exception as e:
            assert e is not None

def test_get_all_users(db:sqlite3.Connection,existing_book:dict):
    assert isinstance(db, sqlite3.Connection)

    books= get_users(None) 
    assert len(books)  > 0


def test_get_all_users_invalid_field(db:sqlite3.Connection):
    assert isinstance(db, sqlite3.Connection)
    try:
        get_users({"invalid_field":"invalid_field_value"})
        assert False, "should throw exception that field is invalid"
    except Exception as e:
        isinstance(e, AssertionError)