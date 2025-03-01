import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify
)

from app.db import get_db
from app.repository.book import (get_books)
from app.messaging.sync.frontend_service import (get_users_from_frontend)

bp = Blueprint('borrow_list', __name__)

@bp.route('/', methods=("GET",))
def list_of_users_and_books_borrowed():
        
        borrowed_books=get_books(filters={"is_available": False})
        if not borrowed_books:
                return jsonify({"data":[]})
        
        ids=[rec.get("user_id") for rec in borrowed_books]
        for id in ids:
                list_str=str(id)+","
        users=get_users_from_frontend(filters={"ids": list_str})
        for user in users:
                for book in borrowed_books:
                        if book.get("user_id")==user.get("id"):
                                book["user"]=user
        return jsonify({"data":users})

