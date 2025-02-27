from admin_backend_service.messaging.rmq.rabbitmq_conn import get_channel 
def setup_topic_users_exchange_and_queues():
    ch=get_channel()
    ch.exchange_declare(exchange='users', exchange_type='topic')
    ch.queue_declare(queue='users')
    ch.queue_bind(exchange='users', queue='users', routing_key='users.*')
    ch.queue_bind(exchange='users', queue='users', routing_key='users.update_user')