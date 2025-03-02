from app.messaging.rmq.rabbitmq_conn import get_channel 
import json

def publish(exchange,routing_key, payload:dict):
    ch=get_channel()
    payload_str=json.dumps(payload)
    ch.basic_publish(
        exchange=exchange,
        routing_key=routing_key,
        body=payload_str)

def publish_new_book(book):
    publish(
        exchange='topic_books', 
        routing_key='books.new_book', 
        payload=book)

def publish_update_book(book_updates):
    publish(
        exchange="topic_books", 
        routing_key="books.updated_book", 
        payload=book_updates)
    


