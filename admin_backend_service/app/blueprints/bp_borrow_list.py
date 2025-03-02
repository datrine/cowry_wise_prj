from flask import (
    Blueprint,jsonify
)

from app.repository.borrow_list import (get_borrow_list)

bp = Blueprint('borrow_list', __name__)

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

