import pika
from flask import (current_app,g)
def setup_conn():
    if 'rabbitmq_connection' in g and g.rabbitmq_connection.is_open:
        return g.rabbitmq_connection
    connection = pika.BlockingConnection( pika.ConnectionParameters(
        host=current_app.config.get("RABBITMQ_SERVER"),
        port=current_app.config.get("RABBITMQ_PORT"),
        virtual_host=current_app.config.get("RABBITMQ_VHOST"),
        credentials=pika.PlainCredentials(
            username=current_app.config.get("RABBITMQ_USER"),
            password=current_app.config.get("RABBITMQ_PASS")
            )))
    g.rabbitmq_connection=connection
    return connection
#channel=None

def get_channel():
    #global channel
    #if channel is not None and channel.is_open() is True:
    #    return channel
    conn = setup_conn()
    channel = conn.channel()
    channel.is_open
    return channel


