import requests

from flask import current_app, g

def get_base_url():
    with current_app.app_context():
        base_url=current_app.config.get("ADMIN_SERVER_URL")
    return base_url

def get_book_by_id_request(id):
    res=requests.get(f"{get_base_url()}/books/{id}")
    if res.status_code>=400:
        raise Exception(f"failed to get book by id: {id}")
    res_book=res.json()
    return res_book.get("data")

def update_book_by_id_request(id,data):
    print(data)
    res=requests.put(f"{get_base_url()}/books/{id}",json=data,headers={"Content-Type": "application/json"})
    if res.status_code>=400:
        raise Exception(f"failed to update book with id: {id}")
    res_book=res.json()
    return res_book.get("data")

def get_books_request(filter:dict):
    res=requests.get(f"{get_base_url()}/books",{
        "is_available":filter.get("is_available"),
        "category":filter.get("category"),
        "publisher":filter.get("publisher")})
    if res.status_code>=400:
        raise Exception("failed to get books"+"" if filter is None else f" with filter: {filter}")
    res_filterable_books=res.json()
    return res_filterable_books.get("data")