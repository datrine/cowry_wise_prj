import threading
import os
import app.messaging as messaging
import app.messaging.rmq.consumer as msg_consumer

from flask import Flask

def create_app(test_config=None):
    app= Flask(__name__, instance_relative_config=True)

    config_app(app=app, test_config= test_config)

    if test_config is not None:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    return app


def config_app(app:Flask, test_config=None):
    if test_config is not None:
        app.config.from_mapping(test_config)
        return
    else:
        app.config["DATABASE_URL"]=os.getenv('DATABASE_URL') if os.getenv('DATABASE_URL')  else  os.path.join('frontend_db.sqlite')
        app.config["SECRET_KEY"]= os.getenv('SECRET_KEY') if os.getenv('SECRET_KEY') else'dev',
        app.config["ADMIN_SERVER_URL"]=os.getenv('ADMIN_SERVER_URL') if os.getenv('ADMIN_SERVER_URL') else "http://localhost:5000"
        app.config["RABBITMQ_URL"]=os.getenv('RABBITMQ_URL') if os.getenv('RABBITMQ_URL') else "amqp://localhost:5672"
        app.config["RABBITMQ_SERVER"]=os.getenv('RABBITMQ_SERVER') if os.getenv('RABBITMQ_SERVER') else "localhost"
        app.config["RABBITMQ_PORT"]=os.getenv('RABBITMQ_PORT') if os.getenv('RABBITMQ_PORT') else 5672
        app.config["RABBITMQ_USER"]=os.getenv('RABBITMQ_USER') if os.getenv('RABBITMQ_USER') else "guest"
        app.config["RABBITMQ_PASS"]=os.getenv('RABBITMQ_PASS') if os.getenv('RABBITMQ_PASS') else "guest"
        app.config["RABBITMQ_VHOST"]=os.getenv('RABBITMQ_VHOST') if os.getenv('RABBITMQ_VHOST') else "/"
    return









#"""import threading
#import os
#from app.app import create_app
#import app.messaging as messaging
#import app.messaging.consumer as msg_consumer

#from flask import Flask
#app=create_app()
#if __name__ == "__main__":
#    app.run(debug=True)
#from . import db
#with app.app_context():
#    db.init_app(app)
#    db.init_db()
#    messaging.init()


#t1=threading.Thread(target=msg_consumer.consume,args=(app,))
#t1.start()
#t1.join()

#"""