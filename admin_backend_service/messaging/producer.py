from admin_backend_service.messaging.rmq.rabbitmq_conn import get_channel 
import json
def publish(exchange,routing_keys, payload:dict):
    ch=get_channel()
    payload_str=json.dumps(payload)
    ch.basic_publish(exchange=exchange,routing_key=routing_keys,body=payload_str)





