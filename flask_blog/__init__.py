from logging import DEBUG
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config
from authlib.integrations.flask_client import OAuth


db = SQLAlchemy()
bcrypt = Bcrypt()
mail = Mail()
oauth = OAuth()


login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    oauth.init_app(app)

    from flask_blog.users.routes import users
    from flask_blog.main.routes import main
    from flask_blog.posts.routes import posts

    app.register_blueprint(users)
    app.register_blueprint(main)
    app.register_blueprint(posts)

    return app
