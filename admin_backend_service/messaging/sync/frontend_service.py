import requests

from flask import current_app, g,Flask

def get_base_url():
    with current_app.app_context():
        base_url=current_app.config.get("FRONTEND_SERVER_URL")
    return base_url
def get_users_from_frontend(filters):
    res=requests.get(f"{get_base_url()}/users",params=filters)
    if res.status_code>=400:
        raise Exception("failed to get users")
    res_user=res.json()
    return res_user.get("data")


def get_borrow_list_from_frontend(filters):
    res=requests.get(f"{get_base_url()}/borrow_list",params=filters)
    if res.status_code>=400:
        raise Exception("failed to get borrow list")
    res_borrow_list=res.json()
    return res_borrow_list.get("data")