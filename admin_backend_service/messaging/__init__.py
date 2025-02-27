#import flask
from admin_backend_service.messaging.rmq.rabbit_mq_utils import setup_topic_users_exchange_and_queues

def init():
    setup_topic_users_exchange_and_queues()
    print("Messaging")
