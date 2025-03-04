from datetime import (datetime,timedelta)

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify
)

from app.repository.book import (save_book,get_books,delete_book_by_id,get_book_by_id,update_book_by_id)
from app.messaging.rmq.publishers import (publish_new_book,publish_delete_book)

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

@bp.route('/status/unavailable', methods=("GET",))
def get_unavailable_books_handler():
        try:
            books_found=get_books(filters={
                                           "is_available":False})
            print(books_found)
            if len(books_found) == 0:
                return jsonify({"data":[]}),200
            for book in books_found:
                book["date_available"]=(datetime.fromisoformat(book.get("return_date"))+timedelta(days=1)).isoformat()
            return jsonify({"data":books_found}),200
        except Exception as e:
            return jsonify({"message":str(e)}),400

@bp.route('/', methods=("POST",))
def add_book_handler():
        body_as_json = request.get_json(force=False)
        title=body_as_json.get('title')
        publisher = body_as_json.get('publisher')
        category = body_as_json.get('category')

        if not title:
            return jsonify({"message":'title is required.'}),400
        elif not publisher:
            return jsonify({"message":'publisher is required.'}),400
        elif not category:
            return jsonify({"message":'category is required.'}),400
        
        book_created=save_book(title=title,publisher=publisher,category=category)
        publish_new_book(book=book_created)
        return jsonify({"data":book_created}),201

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

@bp.route('/<id>', methods=("PUT",))
def update_book_handler(id):
        if not id:
            return jsonify({"message":'id is required.'}),400
        body_as_json = request.get_json(force=False)

        try:
             category_update=body_as_json.get('category')
        except Exception as e:
            return jsonify({"message":str(e)}),400
        
        try:
             publisher_update=body_as_json.get('publisher')
        except Exception as e:
            return jsonify({"message":str(e)}),400
        
        try:
             is_available_update=body_as_json.get('is_available')
        except Exception as e:
            return jsonify({"message":str(e)}),400
        
        try:
             return_date_update=body_as_json.get('return_date')
             if return_date_update is not None:
                  print(return_date_update)
                  return_date_update=datetime.fromisoformat(return_date_update)
        except Exception as e:
            return jsonify({"message":f"return date invalid: {str(e)}"}),400
        
        try:
             loan_date_update=body_as_json.get('loan_date')
             if loan_date_update is not None:
                  loan_date_update=datetime.fromisoformat(loan_date_update)
        except Exception as e:
            return jsonify({"message":f"loan date {str(e)}"}),400
        
        try:
            print("Success")
            book_updated=update_book_by_id(id=id,update_fields={
                 "is_available":is_available_update,
                 "category":category_update,
                 "publisher":publisher_update,
                 "return_date":datetime.isoformat(return_date_update) if return_date_update is not None else None ,
                 "loan_date": datetime.isoformat(loan_date_update) if loan_date_update is not None else None,
                 })
            #publish_update_book(book_updates={
                 #"id":id,
                 #"updates":{
                 #   "is_available":is_available_update,
                 #   "category":category_update,
                 #   "publisher":publisher_update,
                 #   "return_date":datetime.isoformat(return_date_update) if return_date_update is not None else None ,
                 #   "loan_date": datetime.isoformat(loan_date_update) if loan_date_update is not None else None,
                 #}
            #})
            return jsonify({"data":book_updated}),200
        except Exception as e:
            return jsonify({"message":f"book with id {id} failed to update.{str(e)}"}),400


@bp.route('/<id>', methods=("DELETE",))
def delete_book_handler(id):

        if not id:
            return jsonify({"message":'id is required.'}),400
        try:
            book_created=delete_book_by_id(id=id)
            if not book_created:
                return jsonify({"message":f"book with id {id} not found."}),404
        except Exception as e:
            return jsonify({"message":str(e)}),400
        publish_delete_book(book_id_payload={
            "id":id
        })
        return jsonify({"message":f"book with id {id} deleted."}),200

