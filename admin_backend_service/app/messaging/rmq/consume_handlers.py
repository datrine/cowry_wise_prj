import json
from datetime import datetime
from app.repository.user import (save_user,update_user_by_id)
from app.repository.book import (save_book,update_book_by_id)
from app.repository.borrow_list import (save_borrow_list_item)
import logging
mylogger = logging.getLogger("MyLogger")
from flask import Flask
from app.messaging.rmq.rabbitmq_conn import get_channel

def consume(app:Flask):
    with app.app_context():
        ch=get_channel()
        ch.basic_consume(
            queue="queue_new_users", 
            on_message_callback= new_user_message_handler,auto_ack=True)
        ch.basic_consume(
            queue="queue_updated_books",
            on_message_callback= updated_book_message_handler,auto_ack=True)
        ch.basic_consume(
            queue="queue_new_borrow_list_items",
            on_message_callback= new_borrow_list_item_message_handler,auto_ack=True)
        print("Consumer started")
        ch.start_consuming()

def new_user_message_handler(ch, method, properties, body):
    user=json.loads(body)
    mylogger.info(user)
    print(user)
    print("queue_new_users started")
    try:
        save_user(
            email=user.get('email'),
            firstname=user.get('firstname'),
            lastname=user.get('lastname')
            )
        #ch.basic_ack()
    except Exception as e:
        mylogger.error(e)

#def updated_user_message_handler(ch, method, properties, body):
#    user=json.loads(body)
#    mylogger.info(user)
#    try:
#        update_user_by_id(id=user.get('user_id'),update_fields={
#            "email":user.get('updates').get('email'),
#            "lastname":user.get('updates').get('lastname'),
#            "firstname":user.get('updates').get('firstname'),
#            })
#    except Exception as e:
#        mylogger.error(e)
    
def new_borrow_list_item_message_handler(ch, method, properties, body):
    input=json.loads(body)
    print(body)
    try:
        save_borrow_list_item( {       
            "book_id":input.get('book_id'),
            "user_id":input.get('user_id'),
            "email":input.get('email'),
            "firstname":input.get('firstname'),
            "lastname":input.get('lastname'),
            "title":input.get('title'),
            "category":input.get('category'),
            "publisher":input.get('publisher'),
            "is_available":input.get('is_available'),
            "loan_date":datetime.fromisoformat( input.get('loan_date')),
            "return_date":datetime.fromisoformat(input.get('return_date')),
            }
        )
        #ch.basic_ack()
        ch.confirm_delivery()
    except Exception as e:
        mylogger.error(e)

def updated_book_message_handler(ch, method, properties, body):
    book=json.loads(body)
    try:
        update_book_by_id(id=book.get('id'),update_fields={
            "title":book.get('updates').get('email'),
            "category":book.get('updates').get('category'),
            "publisher":book.get('updates').get('publisher'),
            "loan_date":book.get('updates').get('loan_date'),
            "return_date":book.get('updates').get('return_date'),
            "is_available":book.get('updates').get('is_available'),
            })
    except Exception as e:
        print(e)
        mylogger.error(e)
    
#def new_book_message_handler(ch, method, properties, body):
#    book=json.loads(body)
#    mylogger.info(body)
#    save_book(
#        title=book.get('title'),
#        category=book.get('category'),
#        publisher=book.get('publisher'),
#        loan_date=book.get('loan_date'),
#        return_date=book.get('return_date')
#        )

#def updated_book_message_handler(ch, method, properties, body):
#    book=json.loads(body)
#    mylogger.info(book)
#    update_book_by_id(id=book.get('id'),update_fields={
#        "title":book.get('updates').get('email'),
#        "category":book.get('updates').get('category'),
#        "publisher":book.get('updates').get('publisher'),
#        "loan_date":book.get('updates').get('loan_date'),
#        "return_date":book.get('updates').get('return_date'),
#        })