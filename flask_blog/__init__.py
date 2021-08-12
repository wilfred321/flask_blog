from logging import DEBUG
from flask import Flask
from flask_sqlalchemy import SQLAlchemy




app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SECRET_KEY'] = '63f4ce6948a9d40a72191bb94b9c23fb'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from flask_blog import routes