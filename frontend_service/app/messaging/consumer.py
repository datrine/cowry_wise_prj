from app.messaging.rmq.rabbitmq_conn import get_channel 
from app.messaging.async_msg.consume_handlers import (
    new_book_message_handler,
    new_user_message_handler,
    updated_book_message_handler,
    updated_user_message_handler) 
import json

async def consume(queue, callback):
    ch=get_channel()
    ch.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    ch.basic_consume(
        queue="queue_new_users", 
        callback= new_user_message_handler)
    ch.basic_consume(
        queue="queue_updated_users",
        callback= updated_user_message_handler)
    ch.basic_consume(
        queue="queue_new_books",
        callback= new_book_message_handler)
    ch.basic_consume(
        queue="queue_updated_books",
        callback= updated_book_message_handler)
    ch.start_consuming()