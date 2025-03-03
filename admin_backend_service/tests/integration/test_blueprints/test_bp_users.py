from app.blueprints.bp_users import list_of_users_handler
from flask import Flask
import faker
fake=faker.Faker()

def test_list_of_users_handler(app:Flask):

    with app.test_request_context():
        [res,status]=list_of_users_handler()
        print(res)
        assert status==200
        res_data=res.get_json()
        assert res_data.get("data") is not None
        res_data_data=res_data.get("data")
        assert res_data_data is not None
