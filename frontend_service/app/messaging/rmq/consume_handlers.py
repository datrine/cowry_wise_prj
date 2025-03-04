import json
from app.repository.user import (save_user,update_user_by_id)
from app.repository.book import (save_book,update_book_by_id,delete_book_by_id)
import logging
mylogger = logging.getLogger("MyLogger")
    
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

def deleted_book_message_handler(ch, method, properties, body):
    book=json.loads(body)
    mylogger.info(book)
    print(book)
    try:
        delete_book_by_id(id=book.get('id'),)
    except Exception as e:
        mylogger.error(e)