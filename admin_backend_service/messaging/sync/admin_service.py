import requests

from flask import current_app, g
base_url=current_app.config.get("ADMIN_SERVER_URL")
def get_user_by_id(id):
    res=requests.get(f"{base_url}/{id}")
    user=res.json()
    return user