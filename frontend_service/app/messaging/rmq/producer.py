from app.messaging.rmq.rabbitmq_conn import get_channel 
import json
def publish(exchange,routing_key, payload:dict):
    ch=get_channel()
    payload_str=json.dumps(payload)
    ch.basic_publish(exchange=exchange,routing_key=routing_key,body=payload_str)
    print("Published to exchange: " + 
          exchange + " routing key: " +
          routing_key + " with payload: " + payload_str)





