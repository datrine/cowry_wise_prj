from app.blueprints.bp_users import register_handler ,list_of_users_handler
from flask import Flask
import faker
fake=faker.Faker()
def test_register_handler(app:Flask):
    data={
        "email":fake.email(),
        "password":fake.password(),
        "firstname":fake.first_name(),
        "lastname":fake.last_name()
    }
    with app.test_request_context(json=data):
        [res,status]=register_handler()
        assert status==201
        res_data=res.get_json()
        assert res_data.get("data") is not None
        res_data_data=res_data.get("data")
        assert res_data_data.get("email") is not None
        assert res_data_data.get("id") is not None
        assert res_data_data.get("firstname") is not None
        assert res_data_data.get("lastname") is not None
        assert res_data_data.get("email") == data.get("email")
        assert res_data_data.get("firstname") == data.get("firstname")
        assert res_data_data.get("lastname") == data.get("lastname")


        
def test_register_handler_email_missing_error_response(app:Flask):
    data={
        "email":None,
        "password":fake.password(),
        "firstname":fake.first_name(),
        "lastname":fake.last_name()
    }
    with app.test_request_context(json=data):
        [res,status]=register_handler()
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None

        
def test_register_handler_firstname_missing_error_response(app:Flask):
    data={
        "email":fake.password(),
        "firstname":None,
        "lastname":fake.last_name()
    }
    with app.test_request_context(json=data):
        [res,status]=register_handler()
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None

                
def test_register_handler_lastname_missing_error_response(app:Flask):
    data={
        "email":fake.password(),
        "firstname":None,
        "lastname":fake.last_name()
    }
    with app.test_request_context(json=data):
        [res,status]=register_handler()
        assert status==400
        res_data=res.get_json()
        assert res_data.get("data") is None


def test_list_of_users_handler(app:Flask):

    with app.test_request_context():
        [res,status]=list_of_users_handler()
        print(res)
        assert status==200
        res_data=res.get_json()
        assert res_data.get("data") is not None
        res_data_data=res_data.get("data")
        assert res_data_data is not None
