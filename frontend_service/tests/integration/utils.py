import pika
from flask import (current_app,g)
def cleanup_rmq():
    if 'rabbitmq_connection' in g and g.rabbitmq_connection.is_open:
        conn= g.rabbitmq_connection
    else:
        conn = pika.BlockingConnection( pika.ConnectionParameters(
            host=current_app.config.get("RABBITMQ_SERVER"),
            port=current_app.config.get("RABBITMQ_PORT"),
            virtual_host=current_app.config.get("RABBITMQ_VHOST"),
            credentials=pika.PlainCredentials(
                username=current_app.config.get("RABBITMQ_USER"),
                password=current_app.config.get("RABBITMQ_PASS")
                )))
    channel = conn.channel()
    #channel.exchange_unbind(queue="topic_users")
    channel.exchange_delete(exchange="topic_users")
    channel.exchange_delete(exchange="topic_books")
    channel.exchange_delete(exchange="topic_borrow_list_items")
    channel.queue_delete(queue="queue_users")
    channel.queue_delete(queue="queue_new_users")
    channel.queue_delete(queue="queue_updated_users")
    channel.queue_delete(queue="queue_books")
    channel.queue_delete(queue="queue_new_books")
    channel.queue_delete(queue="queue_updated_books")
    channel.queue_delete(queue="queue_borrow_list_items")
    channel.queue_delete(queue="queue_new_borrow_list_items")
    channel.queue_delete(queue="queue_updated_borrow_list_items")
    g.rabbitmq_connection=conn
    return conn