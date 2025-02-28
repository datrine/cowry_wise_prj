from frontend_service.messaging.producer import publish
def update_user(user):
    publish(exchange="topic_users", routing_keys="update", payload=user)


