from flask import Flask
from app.messaging.rmq.rabbitmq_conn import get_channel 
from app.messaging.rmq.consume_handlers import (
    new_book_message_handler,
    deleted_book_message_handler,) 
ch=None
def consume(app:Flask):
    with app.app_context():
        ch=get_channel()
        #ch.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
        ch.basic_consume(
            queue="queue_new_books",
            on_message_callback= new_book_message_handler,auto_ack=True)
        ch.basic_consume(
            queue="queue_deleted_books",
            on_message_callback= deleted_book_message_handler,auto_ack=True)
        ch.start_consuming()