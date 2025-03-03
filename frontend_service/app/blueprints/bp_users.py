from flask import (
    Blueprint, request,jsonify
)

from app.repository.user import (save_user,get_users,get_users_by_ids)
from app.messaging.rmq.publishers import (
    publish_new_user,)

bp = Blueprint('users', __name__,)

@bp.route('/register', methods=("POST",))
def register_handler():
    body_as_json = request.get_json(force=False)
    email=body_as_json.get('email')
    firstname = body_as_json.get('firstname')
    lastname = body_as_json.get('lastname')
    #print(body_as_json)
    if not email:
        return jsonify({"message":'email is required.'}),400
    elif not firstname:
        return jsonify({"message":'Firstname is required.'}),400
    elif not lastname:
        return jsonify({"message":'Lastname is required.'}),400
    print(email, firstname, lastname)
    user_created=save_user(email=email,firstname=firstname,lastname=lastname)
    publish_new_user(user_created)
    return jsonify({"data":user_created}),201



@bp.route('/', methods=("GET",))
def list_of_users_handler():
    try:
        #ids=request.args.get('ids')
        #print(ids)
        #if ids is not None:
        #    ids=ids.split(',')
        #    users=get_users_by_ids(filters=tuple(ids))
        #else:
        users=get_users(filters=None)
    
        return jsonify({"data":users}),200
    except Exception as e:
        return jsonify({"message":str(e)}),400



