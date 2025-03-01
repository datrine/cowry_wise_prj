from app.repository.user import (save_user,update_user_by_id)
from app.repository.book import (save_book,update_book_by_id)

def new_user_message_handler(user:dict):
    save_user(
        email=user.get('email'),
        firstname=user.get('firstname'),
        lastname=user.get('lastname')
        )

def updated_user_message_handler(user:dict):
    update_user_by_id(id=user.get('user_id'),update_fields={
        "email":user.get('updates').get('email'),
        "lastname":user.get('updates').get('lastname'),
        "firstname":user.get('updates').get('firstname'),
        })
    

    
def new_book_message_handler(user:dict):
    save_book(
        title=user.get('title'),
        category=user.get('category'),
        publisher=user.get('publisher'),
        loan_date=user.get('loan_date'),
        return_date=user.get('return_date')
        )

def updated_book_message_handler(user:dict):
    update_book_by_id(id=user.get('id'),update_fields={
        "title":user.get('updates').get('email'),
        "category":user.get('updates').get('category'),
        "publisher":user.get('updates').get('publisher'),
        "loan_date":user.get('updates').get('loan_date'),
        "return_date":user.get('updates').get('return_date'),
        })