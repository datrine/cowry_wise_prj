from flask import (
    Blueprint,jsonify
)

from frontend_service.messaging.sync.admin_service import (get_books_request,get_book_by_id_request)

bp = Blueprint('books', __name__,)


@bp.route('/<id>', methods=("GET",))
def get_book_by_id(id):
        
        book_created=get_book_by_id_request(id=id)
        
        return jsonify({"data":book_created}),200


@bp.route('/status/available', methods=("GET",))
def get_available_books():
        try:
            book_created=get_books_request({"is_available":True})
            return jsonify({"data":book_created}),200
        except Exception as e:
            return jsonify({"message":str(e)}),400

