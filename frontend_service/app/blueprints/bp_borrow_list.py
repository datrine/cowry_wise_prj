from datetime import datetime

from flask import (
    Blueprint, request, jsonify
)

from app.repository.user import (get_user_by_id)
#from app.messaging.sync.admin_service import (get_book_by_id_request,update_book_by_id_request)
from app.repository.borrow_list import (save_borrow_list_item,get_borrow_list,)
from app.repository.user import (get_user_by_id)
from app.repository.book import (get_book_by_id,update_book_by_id)
from app.messaging.rmq.publishers import (
    publish_new_borrow_list_item,publish_update_book)

bp = Blueprint('borrow_list', __name__,)

@bp.route('/', methods=("GET",))
def list_of_users_and_books_borrowed_handler():
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
    return jsonify({"data":items}),200

@bp.route('/', methods=("POST",))
def borrow_book_handler():
    try:
        body_as_json = request.get_json(force=False)
    except Exception as e:
        return jsonify({"message":str(e)}),400
    
    try:
        return_date_raw = body_as_json.get('return_date')
        if not return_date_raw:
            return jsonify({"message":'return_date is required. Date must be in ISO 8601'}),400
        return_date = datetime.fromisoformat(return_date_raw)
    except Exception as e:
        print(e)
        return jsonify({"message":str(e)}),400
    
    try:
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
            return jsonify({"message":'user does not exist'}),404
    except Exception as e:
        return jsonify({"message":str(e)}),400  
    
    try:
        book = get_book_by_id(id=book_id)
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
            "book_id":book_id,
            "email":user.get("email"),
            "firstname":user.get("firstname"),
            "lastname":user.get("lastname"),
            "title":book.get("title"),
            "category":book.get("category"),
            "publisher":book.get("publisher"),
            "return_date":return_date
            })
    
    update_book_by_id(id=book_id,update_fields={
        "is_available":False,
        "return_date":return_date.isoformat(),
        "loan_date":borrow_info.get("loan_date").isoformat(),
        })
    """
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
    """
    publish_update_book(book_updates={
        "id":book_id,
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