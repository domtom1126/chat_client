from flask import Flask
from flask_socketio import SocketIO, send
import json
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    socketio = SocketIO(app)

    @socketio.on('message')
    def handleMessage(msg):
        print('Message: ' + msg)
        send(msg, broadcast=True)

# SECTION This is for production
#     # with open('/etc/config.json') as config_file:
#     #     config = json.load(config_file)

#     # app.config['SECRET_KEY'] = config.get('SECRET_KEY')
#     # app.config['SQLALCHEMY_DATABASE_URI'] = config.get('SQLALCHEMY_DATABASE_URI')
# !SECTION End of production stuff

    app.config['SECRET_KEY'] = '1234'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))


    # Blueprint for auth routes
    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # Blueprint for non-auth
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
