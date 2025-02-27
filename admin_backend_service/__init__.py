import os
import admin_backend_service.messaging as messaging
#from admin_backend_service. messaging.async_msg.consume_handlers import register_handlers

from flask import Flask

def create_app(test_config=None):
    app= Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/health')
    def hello():
        return 'Service is up!'
    
    from . import db
    db.init_app(app)

    # import users blueprint
    from . import bp_users
    app.register_blueprint(bp_users.bp,url_prefix='/users')

    # import books blueprint
    from . import bp_books
    app.register_blueprint(bp_books.bp)
    messaging.init()
    #register_handlers()
    return app