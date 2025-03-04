from app.messaging.rmq.producer import publish

def publish_new_user(user):
    publish(exchange="topic_users", routing_key="users.new_user", payload=user)
    
#def publish_update_user(user):
#    publish(
#        exchange="topic_users", routing_key="users.updated_user", payload=user)

def publish_update_book(book_updates):
    print("book_updates: ",book_updates)
    publish(
        exchange="topic_books", 
        routing_key="books.updated_book", 
        payload=book_updates)
    
def publish_new_borrow_list_item(new_borrow_list_item):
    publish(
        exchange="topic_borrow_list_items", 
        routing_key="borrow_list_items.new_borrow_list_item", 
        payload=new_borrow_list_item)
