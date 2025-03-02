from app.messaging.rmq.rabbitmq_conn import get_channel 
def setup_topic_users_exchange_and_queues():
    ch=get_channel()
    ch.exchange_declare(exchange='topic_users', exchange_type='topic')
    ch.queue_declare(queue='queue_users')
    ch.queue_declare(queue='queue_new_users')
    ch.queue_declare(queue='queue_updated_users')
    ch.queue_bind(exchange='topic_users', queue='queue_users', routing_key='users.*')
    ch.queue_bind(exchange='topic_users', queue='queue_new_users', routing_key='users.new_user')
    ch.queue_bind(exchange='topic_users', queue='queue_updated_users', routing_key='users.updated_user')

    
def setup_topic_books_exchange_and_queues():
    ch=get_channel()
    ch.exchange_declare(exchange='topic_books', exchange_type='topic')
    ch.queue_declare(queue='queue_books')
    ch.queue_declare(queue='queue_new_books')
    ch.queue_declare(queue='queue_updated_books')
    ch.queue_bind(exchange='topic_books', queue='queue_books', routing_key='books.*')
    ch.queue_bind(exchange='topic_books', queue='queue_new_books', routing_key='books.new_book')
    ch.queue_bind(exchange='topic_books', queue='queue_updated_books', routing_key='books.updated_book')


    
def setup_topic_borrow_list_exchange_and_queues():
    ch=get_channel()
    ch.exchange_declare(exchange='topic_borrow_list_items', exchange_type='topic')
    ch.queue_declare(queue='queue_borrow_list_items')
    ch.queue_declare(queue='queue_new_borrow_list_items')
    ch.queue_declare(queue='queue_updated_borrow_list_items')
    ch.queue_bind(
        exchange='topic_borrow_list_items', 
        queue='queue_borrow_list_items', 
        routing_key='borrow_list_items.*')
    ch.queue_bind(
        exchange='topic_borrow_list_items', 
        queue='queue_new_borrow_list_items', 
        routing_key='borrow_list_items.new_borrow_list_item')
    ch.queue_bind(
        exchange='topic_borrow_list_items', 
        queue='queue_updated_borrow_list_items', 
        routing_key='borrow_list_items.updated_borrow_list_item')