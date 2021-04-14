# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
# For relative imports to work in Python 3.6
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    
    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'    
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ttokbpjecjcqpu:a7874a1181e570148dad232916ac5809b0d8d5e945364755808a10c7ac578ab3@ec2-34-195-233-155.compute-1.amazonaws.com:5432/d9aig6f88lt429'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from models import User    

    @login_manager.user_loader    
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for non-auth parts of app
    from games import games as main_blueprint
    app.register_blueprint(main_blueprint)

    # blueprint for non-auth parts of app
    from ml_utils import ml_utils as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
