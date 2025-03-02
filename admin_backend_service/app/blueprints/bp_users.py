import requests
from flask import (
    Blueprint, request,jsonify
)
from app.repository.user import (save_user,get_users,get_users_by_ids)

#from app.db import get_db
from app.messaging.sync.frontend_service import (get_users_from_frontend)

bp = Blueprint('users', __name__)

#@bp.route('/', methods=("GET",))
#def list_of_users():
#    try:
#        users=get_users_from_frontend(filters=None)
#        return jsonify({"data":users})
#    except Exception as e:
#        return jsonify({"error":str(e)}),400

@bp.route('/', methods=("GET",))
def list_of_users():
    try:
        ids=request.args.get('ids')
        print(ids)
        if ids is not None:
            ids=ids.split(',')
            users=get_users_by_ids(filters=tuple(ids))
        else:
            users=get_users(filters=None)
    
        return jsonify({"data":users})
    except Exception as e:
        return jsonify({"message":str(e)}),400