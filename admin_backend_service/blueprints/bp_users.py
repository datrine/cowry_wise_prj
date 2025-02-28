import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify
)

#from admin_backend_service.db import get_db
from admin_backend_service.messaging.sync.frontend_service import (get_users_from_frontend)

bp = Blueprint('users', __name__)

@bp.route('/', methods=("GET",))
def list_of_users():
    try:
        users=get_users_from_frontend(filters=None)
        return jsonify({"data":users})
    except Exception as e:
        return jsonify({"error":str(e)}),400

