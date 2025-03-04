from flask import (
    Blueprint, request,jsonify
)
from app.repository.user import (get_users)

bp = Blueprint('users', __name__)

@bp.route('/', methods=("GET",))
def list_of_users_handler():
    try:
        ids=request.args.get('ids')
        print(ids)
        if ids is not None:
            ids=ids.split(',')
            users=get_users_by_ids(filters=tuple(ids))
        else:
            users=get_users(filters=None)
    
        return jsonify({"data":users}),200
    except Exception as e:
        return jsonify({"message":str(e)}),400