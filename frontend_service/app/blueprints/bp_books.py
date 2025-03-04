from datetime import datetime

from flask import (
    Blueprint,  request, jsonify
)

from app.repository.book import (get_books,get_book_by_id)
from app.repository.user import (get_user_by_id)

from app.repository.book import (get_book_by_id,update_book_by_id)
from app.repository.borrow_list import (save_borrow_list_item,get_borrow_list,)
from app.messaging.rmq.publishers import (
    publish_new_borrow_list_item,publish_update_book)
from datetime import timedelta

bp = Blueprint('books', __name__,)

@bp.route('/', methods=("GET",))
def get_books_handler():
        try:
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


@bp.route('/status/available', methods=("GET",))
def get_available_books_handler():
        try:
            books_found=get_books(filters={
                                           "is_available":True})
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
            book_found=get_book_by_id(id=id)
            if not book_found:
                return jsonify({"message":f"book with id {id} not found."}),404
            
            return jsonify({"data":book_found}),200
        except Exception as e:
            return jsonify({"message":str(e)}),500



@bp.route('/<id>/borrow', methods=("POST",))
def borrow_book_handler(id):
    try:
        body_as_json = request.get_json(force=False)
    except Exception as e:
        return jsonify({"message":str(e)}),400
    
    # validate "borrow_days" & "user_id" fields
    try:
        borrow_days = body_as_json.get('borrow_days')
        if not borrow_days:
            return jsonify({"message":'borrow_days is required. Must be a number'}),400
        return_date = datetime.now() + timedelta(days=borrow_days)
    except Exception as e:
        print(e)
        return jsonify({"message":str(e)}),400
        
    try:
        user_id = body_as_json.get('user_id')
        if not user_id:
            return jsonify({"message":'user id is required.'}),400
    except Exception as e:
        print(e)
        return jsonify({"message":str(e)}),400
    
    # check if the user exists
    try:
        user = get_user_by_id(id=user_id)
        if user is None:
            return jsonify({"message":'user does not exist'}),404
    except Exception as e:
        return jsonify({"message":str(e)}),400  
    
    # check if the book exists and is available
    try:
        book = get_book_by_id(id=id)
        if book is None:
            return jsonify({"message":'book does not exist'}),404
        ret_date=book.get("return_date")
        if ret_date is not None:
            ret_date = datetime.fromisoformat(ret_date)
            if  ret_date > datetime.now():
                return jsonify({"message":'book is not available'}),400
    except Exception as e:
        return jsonify({"message":str(e)}),400
    
    borrow_info = save_borrow_list_item({
            "user_id":user_id, 
            "book_id":id,
            "email":user.get("email"),
            "firstname":user.get("firstname"),
            "lastname":user.get("lastname"),
            "title":book.get("title"),
            "category":book.get("category"),
            "publisher":book.get("publisher"),
            "return_date":return_date
            })
    
    update_book_by_id(id=id,update_fields={
        "is_available":False,
        "return_date":return_date.isoformat(),
        "loan_date":borrow_info.get("loan_date").isoformat(),
        })
    
    publish_new_borrow_list_item(new_borrow_list_item={
        "id":borrow_info.get("id"),
        "user_id":borrow_info.get("user_id"),
        "book_id":borrow_info.get("book_id"),
        "email":borrow_info.get("email"),
        "firstname":borrow_info.get("firstname"),
        "lastname":borrow_info.get("lastname"),
        "title":borrow_info.get("title"),
        "category":borrow_info.get("category"),
        "publisher":borrow_info.get("publisher"),
        "is_available":False,
        "return_date":return_date.isoformat(),
        "loan_date":borrow_info.get("loan_date").isoformat(),
    })
    
    publish_update_book(book_updates={
        "id":id,
        "updates":{
            "is_available":False,
            "return_date":return_date.isoformat(),
            "loan_date":borrow_info.get("loan_date").isoformat(),
            }
        })
    
    return jsonify({"data":{
        "id":borrow_info.get("id"),
        "user_id":borrow_info.get("user_id"),
        "book_id":borrow_info.get("book_id"),
        "email":borrow_info.get("email"),
        "firstname":borrow_info.get("firstname"),
        "lastname":borrow_info.get("lastname"),
        "title":borrow_info.get("title"),
        "category":borrow_info.get("category"),
        "is_available":False,
        "publisher":borrow_info.get("publisher"),
        "return_date":return_date.isoformat(),
        "loan_date":borrow_info.get("loan_date").isoformat(),}}),201
















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