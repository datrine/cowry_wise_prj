import sqlite3

import pytest
from app.db import (get_db,init_app,init_db,close_db)
from flask import Flask

def test_get_close_db(app):
    with app.app_context():
        db = get_db()
        assert db is get_db()
    with pytest.raises(sqlite3.ProgrammingError) as e:
        db.execute('SELECT 1')

    assert 'closed' in str(e.value)


def test_init_app(mocker,app:Flask):
    spy = mocker.spy(app,"teardown_appcontext")
    init_app(app)
    assert spy.call_count == 1
    assert isinstance(app, Flask)

#def test_close_db(mocker,app_context_with_db:AppContext):
#    db=app_context_with_db.g.get("db")
#    spy = mocker.spy(db,"close")
#    close_db()
#    assert spy.call_count == 1
#    assert isinstance(app_context_with_db, AppContext)
#def test_init_db_command():
    #init_db_command()
    #assert 'Initialized' in result.output