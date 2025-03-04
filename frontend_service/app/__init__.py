import threading
from app.app import create_app
import app.messaging as messaging
import app.messaging.rmq.consumer as msg_consumer

from flask import Flask
app=create_app()
if __name__ == "__main__":
    app.run(debug=True)
from . import db
with app.app_context():
    db.init_app(app)
    db.init_db()
    messaging.init()
    # import users blueprint
    from app.blueprints import bp_users
    app.register_blueprint(bp_users.bp,url_prefix='/users')

    # import borrow_list blueprint
    from app.blueprints import bp_borrow_list
    app.register_blueprint(bp_borrow_list.bp,url_prefix='/borrow_list')
    
    # import books blueprint
    from app.blueprints import bp_books
    app.register_blueprint(bp_books.bp,url_prefix='/books')
    t1=threading.Thread(target=msg_consumer.consume,args=(app,),daemon=True)
    try:
        t1.start()
    except KeyboardInterrupt:
        print("\nStopping consumers...")