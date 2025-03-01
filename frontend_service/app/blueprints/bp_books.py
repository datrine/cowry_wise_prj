from datetime import datetime

from flask import (
    Blueprint,  request, jsonify
)

from app.repository.book import (get_books,get_book_by_id)

bp = Blueprint('books', __name__,)


@bp.route('/', methods=("GET",))
def get_books_handler():
        try:
            ids_filter_value=request.args.get('ids')
            if ids_filter_value:
                ids_filter_value=ids_filter_value.split(',')
            category_filter_value=request.args.get('category')
            publisher_filter_value=request.args.get('publisher')
            is_available_filter_value=request.args.get('is_available')
        except Exception as e:
            return jsonify({"message":str(e)}),400
        try:
            books_found=get_books(filters={"category":category_filter_value,
                                           "publisher":publisher_filter_value,
                                           "is_available":is_available_filter_value})
            print(books_found)
            if len(books_found) == 0:
                return jsonify({"data":[]}),200
            return jsonify({"data":books_found}),200
        except Exception as e:
            return jsonify({"message":str(e)}),400

@bp.route('/<id>', methods=("GET",))
def get_book_by_id_handler(id):
        if not id:
            return jsonify({"message":'id is required.'}),400
        try:
            print("SuccessmnkjggcfxdzrzrdzrdzdzerWastdtfyigfiyftycutfdtudrutfdutdrrydydryseatesrdstdyr")
            book_found=get_book_by_id(id=id)
            if not book_found:
                return jsonify({"message":f"book with id {id} not found."}),404
            
            return jsonify({"data":book_found}),200
        except Exception as e:
            return jsonify({"message":str(e)}),400


















"""
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

"""