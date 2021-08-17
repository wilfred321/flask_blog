from logging import DEBUG
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from flask_blog.config import Config


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"


mail = Mail(app)

from flask_blog.users.routes import users
from flask_blog.main.routes import main
from flask_blog.posts.routes import posts


app.register_blueprint(users)
app.register_blueprint(main)
app.register_blueprint(posts)
