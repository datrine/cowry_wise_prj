import os

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

    
    from . import db
    with app.app_context():
        db.init_app(app)
        db.init_db()
        # import users blueprint
        from frontend_service.blueprints import bp_users
        app.register_blueprint(bp_users.bp,url_prefix='/users')

        # import borrow_list blueprint
        from frontend_service.blueprints import bp_borrow_list
        app.register_blueprint(bp_borrow_list.bp,url_prefix='/borrow_list')
        
        # import books blueprint
        from frontend_service.blueprints import bp_books
        app.register_blueprint(bp_books.bp,url_prefix='/books')

        #messaging.init()
        #register_handlers()
    return app


def config_app(app:Flask, test_config=None):
    if test_config is not None:
        app.config.from_mapping(test_config)
        return
    else:
        app.config["DATABASE_URL"]=os.getenv('DATABASE_URL') if os.getenv('DATABASE_URL')  else  os.path.join('frontend_service.sqlite')
        app.config["SECRET_KEY"]= os.getenv('SECRET_KEY') if os.getenv('SECRET_KEY') else'dev',
        app.config["ADMIN_SERVER_URL"]=os.getenv('ADMIN_SERVER_URL') if os.getenv('ADMIN_SERVER_URL') else "http://localhost:5000"
    
    return