from datetime import datetime

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for,jsonify
)

from admin_backend_service.repository.book import (save_book,get_books,delete_book_by_id,get_book_by_id,update_book_by_id)

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
        
        return jsonify({"data":book_created}),201

@bp.route('/<id>', methods=("GET",))
def get_book_handler(id):
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
        print("kgjvhcgxrxrxxhdyfyfu")
        try:
             category_update=body_as_json.get('category')
             publisher_update=body_as_json.get('publisher')
             is_available_update=body_as_json.get('is_available')
             return_date_update=body_as_json.get('return_date')
             if return_date_update is not None:
                  return_date_update=datetime.fromisoformat(return_date_update)
             loan_date_update=body_as_json.get('loan_date')
             if return_date_update is not None:
                  loan_date_update=datetime.fromisoformat(loan_date_update)
        except Exception as e:
            print(e)
            return jsonify({"message":str(e)}),400
        try:
            print("Success")
            book_updated=update_book_by_id(id=id,update_fields={
                 "is_available":is_available_update,
                 "category":category_update,
                 "publisher":publisher_update,
                 "return_date":return_date_update,
                 "loan_date":loan_date_update,
                 })
            if not book_updated:
                return jsonify({"message":f"book with id {id} failed to update."}),404
            
            return jsonify({"data":book_updated}),200
        except Exception as e:
            return jsonify({"message":str(e)}),400


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
        return jsonify({"message":f"book with id {id} deleted."}),200

