from datetime import datetime

from flask import (
    Blueprint, request, jsonify
)

from frontend_service.repository.user import (get_user_by_id)
from frontend_service.messaging.sync.admin_service import (get_book_by_id_request)
from frontend_service.repository.borrow_list import (save_user_book_loan,get_user_book_loans)

bp = Blueprint('borrow_list', __name__,)

@bp.route('/', methods=("GET",))
def list_of_users_and_books_borrowed():
    items = []
    borrow_recs=get_user_book_loans(filters=None)
    #users=get_users_from_frontend(filters={"ids": ids})
    for borrow in borrow_recs:
        if borrow.get("books") is None:
                borrow["books"] =[]
        list(borrow["books"]).append({
                "id": borrow["book_id"],
                "title": borrow.get("title"),
                "publisher": borrow.get("publisher"),
                "category": borrow.get("category"),
                "loan_date": borrow.get("loan_date"),
                "return_date": borrow.get("return_date"),
                })
        borrow.pop("book_id")
        borrow.pop("title")
        borrow.pop("publisher",)
        borrow.pop("category")
        borrow.pop("return_date")
        borrow.pop("loan_date")
        items.append(borrow)
    return jsonify({"data":items})



@bp.route('/', methods=("POST",))
def borrow_book():
    try:
        body_as_json = request.get_json(force=False)
    except Exception as e:
        return jsonify({"message":str(e)}),400
    try:
        return_date_raw = body_as_json.get('return_date')
        if not return_date_raw:
            return jsonify({"message":'return_date is required. Date must be in ISO 8601'}),400
        return_date = datetime.fromisoformat(return_date_raw)
        user_id = body_as_json.get('user_id')
        if not user_id:
            return jsonify({"message":'user id is required.'}),400
        book_id = body_as_json.get('user_id')
        if not book_id:
            return jsonify({"message":'book id is required.'}),400
    except Exception as e:
        print(e)
        return jsonify({"message":str(e)}),400
    
    try:
        user = get_user_by_id(id=user_id)
        if user is None:
            return jsonify({"message":'user does not exist'}),400
    except Exception as e:
        return jsonify({"message":str(e)}),400  
    try:
        book = get_book_by_id_request(id=user_id)
        if book is None:
            return jsonify({"message":'book does not exist'}),400
        if not book["is_available"]:
            return jsonify({"message":'book is not available'}),400
    except Exception as e:
        return jsonify({"message":str(e)}),400  
    borrow_id = save_user_book_loan({
            "user_id":user_id, 
            "book_id":book_id,
            "email":user.get("email"),
            "firstname":user.get("firstname"),
            "lastname":user.get("lastname"),
            "title":book.get("title"),
            "category":book.get("category"),
            "publisher":book.get("publisher"),
            "return_date":return_date
            })

    return jsonify({"data":borrow_id}),201