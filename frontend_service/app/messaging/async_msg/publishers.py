from app.messaging.producer import publish

def publish_new_user(user):
    publish(exchange="topic_users", routing_keys="users.new_user", payload=user)
def publish_update_user(user):
    publish(exchange="topic_users", routing_keys="users.updated_user", payload=user)

def publish_new_books(book):
    publish(exchange='topic_books', routing_keys='books.new_book', payload=book)

def publish_update_books(book):
    publish(exchange="topic_books", routing_keys="books.updated_book", payload=book)


