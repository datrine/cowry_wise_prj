#import flask
from app.messaging.rmq.rabbitmq_conn import (
   setup_conn)
from app.messaging.rmq.rabbit_mq_utils import (
    setup_topic_users_exchange_and_queues,
    setup_topic_books_exchange_and_queues,
    setup_topic_borrow_list_exchange_and_queues)

def init():
    setup_conn()
    setup_topic_users_exchange_and_queues()
    setup_topic_books_exchange_and_queues()
    setup_topic_borrow_list_exchange_and_queues()
    print("Messaging")
