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
    if 'rabbitmq_channel' in g and g.rabbitmq_channel.is_open:
        return g.rabbitmq_channel
    conn = setup_conn()
    g.rabbitmq_channel = conn.channel()
    return g.rabbitmq_channel


