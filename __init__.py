# init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
# For relative imports to work in Python 3.6
import os, sys; sys.path.append(os.path.dirname(os.path.realpath(__file__)))
import re

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    

    try:
        if os.environ.get('SECRET_KEY') == None:
            app.config['SECRET_KEY'] ='9OLWxND4o83j4K4iuopO'
        else:
            app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    except:
        app.config['SECRET_KEY'] ='9OLWxND4o83j4K4iuopO'
    
    uri = os.environ.get("DATABASE_URL")  # or other relevant config var
    
    try:
        if uri.startswith("postgres://"):
            uri = uri.replace("postgres://", "postgresql://", 1)
            app.config['SQLALCHEMY_DATABASE_URI'] = uri
            # rest of connection code using the connection string `uri`    
        else:
            app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Games.db'
    except:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Games.db'    
        
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
 
    with app.app_context():
        db.create_all()
        return app
