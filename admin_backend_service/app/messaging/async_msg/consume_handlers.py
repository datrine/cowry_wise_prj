import asyncio
from app.messaging.consumer import consume
from app.repository.user import (save_user,update_user_by_id)

async def register_handlers():
    add_users_task=asyncio.create_task(
        consume(queue="queue_new_users", 
                callback= new_user_message_handler))
    update_users_task=asyncio.create_task(
        consume(queue="queue_updated_users", 
                callback= updated_user_message_handler)) 
    tasks=[add_users_task,update_users_task]
    async for result in asyncio.as_completed(tasks):
        try:
            result = await result
        except Exception as e:
            print(f"Error: {e}")



def new_user_message_handler(user:dict):
    print(user)
    save_user(email=user.get('email'),
              firstname=user.get('firstname'),
              lastname=user.get('lastname')
        )

def updated_user_message_handler(user:dict):
    update_user_by_id(id=user.get('user_id'),update_fields={
        "email":user.get('updates').get('email'),
        "lastname":user.get('updates').get('lastname'),
        "firstname":user.get('updates').get('firstname'),
        })