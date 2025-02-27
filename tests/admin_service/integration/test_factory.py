import flask
import werkzeug
from admin_backend_service import create_app
#def test_config():
#    assert not create_app().testing
#    assert create_app({'TESTING': True}).testing

def test_health(client:werkzeug.test.Client):
    response= client.get('/health')
    assert response.data == b'Service is up!'