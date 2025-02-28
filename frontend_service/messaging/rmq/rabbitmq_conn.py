import pika
from flask import (current_app,g)
def setup_conn():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=current_app.config.get("RABBITMQ_SERVER"),port=current_app.config.get("RABBITMQ_PORT")))
    return connection
#channel=None

def get_channel():
    #global channel
    #if channel is not None and channel.is_open() is True:
    #    return channel
    channel = setup_conn()
    return channel


