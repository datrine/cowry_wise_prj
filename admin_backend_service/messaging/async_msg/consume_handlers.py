import asyncio
from admin_backend_service.messaging.consumer import consume
from admin_backend_service.repository.user import (save_user,update_user_by_id)

async def register_handlers():
    add_users_task=asyncio.create_task(consume(queue="queue_add_users", callback= add_user_message_handler))
    update_users_task=asyncio.create_task(consume(queue="queue_update_users", callback= update_user_message_handler)) 
    tasks=[add_users_task,update_users_task]
    async for result in asyncio.as_completed(tasks):
        try:
            result = await result
        except Exception as e:
            print(f"Error: {e}")



def add_user_message_handler(user:dict):
    save_user(email=user.get('email'),firstname=user.get('firstname'),lastname=user.get('lastname'))

def update_user_message_handler(user:dict):
    update_user_by_id(id=user.get('user_id'),update_fields={
        "email":user.get('updates').get('email'),
        "lastname":user.get('updates').get('lastname'),
        "firstname":user.get('updates').get('firstname'),
        })