import pytest
from flask import Flask

from admin_backend_service import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    
    yield app


@pytest.fixture
def client(app: Flask):
    return app.test_client()

@pytest.fixture
def runner(app: Flask):
    return app.test_cli_runner()