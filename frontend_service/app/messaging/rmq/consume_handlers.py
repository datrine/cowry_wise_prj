import json
from app.repository.user import (save_user,update_user_by_id)
from app.repository.book import (save_book,update_book_by_id)
import logging
mylogger = logging.getLogger("MyLogger")
#def new_user_message_handler(ch, method, properties, body):
#    user=json.loads(body)
#    mylogger.info(user)
#    save_user(
#        email=user.get('email'),
#        firstname=user.get('firstname'),
#        lastname=user.get('lastname')
#        )

#def updated_user_message_handler(ch, method, properties, body):
#    user=json.loads(body)
#    mylogger.info(user)
#    update_user_by_id(id=user.get('user_id'),update_fields={
#        "email":user.get('updates').get('email'),
#        "lastname":user.get('updates').get('lastname'),
#        "firstname":user.get('updates').get('firstname'),
#        })


    
def new_book_message_handler(ch, method, properties, body):
    book=json.loads(body)
    mylogger.info(body)
    print(book)
    try:
        save_book(
            title=book.get('title'),
            category=book.get('category'),
            publisher=book.get('publisher'),
            loan_date=book.get('loan_date'),
            return_date=book.get('return_date'),
            is_available=book.get('is_available')
            )
    except Exception as e:
        mylogger.error(e)

def updated_book_message_handler(ch, method, properties, body):
    book=json.loads(body)
    mylogger.info(book)
    print(book)
    try:
        update_book_by_id(id=book.get('id'),update_fields={
            "title":book.get('updates').get('email'),
            "category":book.get('updates').get('category'),
            "publisher":book.get('updates').get('publisher'),
            "loan_date":book.get('updates').get('loan_date'),
            "return_date":book.get('updates').get('return_date'),
            })
    except Exception as e:
        mylogger.error(e)