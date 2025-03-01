from datetime import datetime

from flask import (
    Blueprint, request, jsonify
)

from app.repository.user import (get_user_by_id)
from app.messaging.sync.admin_service import (get_book_by_id_request,update_book_by_id_request)
from app.repository.borrow_list import (save_user_book_loan,get_borrow_list,)

bp = Blueprint('borrow_list', __name__,)

@bp.route('/', methods=("GET",))
def list_of_users_and_books_borrowed():
    dic = dict()
    items = []
    borrow_recs=get_borrow_list(filters=None)
    #users=get_users_from_frontend(filters={"ids": ids})
    for borrow in borrow_recs:
        it =dic.get(borrow.get("id"))
        if not it:
           dic[borrow.get("id")] = borrow
           it=dic[borrow.get("id")]
        if it.get("books") is None:
            it["books"] =list()
            print(it)
        it["books"].append({
            "id": it["book_id"],
            "title": it.get("title"),
            "publisher": it.get("publisher"),
            "category": it.get("category"),
            "loan_date": it.get("loan_date"),
            "return_date": it.get("return_date"),
            })
        it.pop("book_id")
        it.pop("title")
        it.pop("publisher",)
        it.pop("category")
        it.pop("return_date")
        it.pop("loan_date")
        print(it)
        items.append(it)
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
        book_id = body_as_json.get('book_id')
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
        book = get_book_by_id_request(id=book_id)
        if book is None:
            return jsonify({"message":'book does not exist'}),400
        print(book)  
        #if not book["is_available"]:
            #return jsonify({"message":'book is not available'}),400
        ret_date=book.get("return_date")
        if ret_date is not None:
            ret_date = datetime.fromisoformat(ret_date)
        if  ret_date>datetime.now():
            return jsonify({"message":'book is not available'}),400
    except Exception as e:
        return jsonify({"message":str(e)}),400
    borrow_info = save_user_book_loan({
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
    update_book_by_id_request(id=book_id,data={
        "is_available":False,
        "return_date":return_date.isoformat(),
        "loan_date":borrow_info.get("loan_date").isoformat(),
        })
    return jsonify({"data":borrow_info}),201