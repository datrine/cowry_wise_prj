import asyncio
from frontend_service.messaging.rmq.rabbitmq_conn import get_channel 
import json

async def consume(queue, callback):
    ch=get_channel()
    ch.basic_consume(queue=queue, on_message_callback=callback, auto_ack=True)
    ch.start_consuming()