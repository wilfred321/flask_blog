from datetime import datetime
<<<<<<< HEAD

from sqlalchemy.orm import backref
from flask_blog import db, login_manager, app
=======
from flask_blog import db, login_manager
from flask import current_app
>>>>>>> app_instances
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
<<<<<<< HEAD
    __tablename__ = "user"
=======
>>>>>>> app_instances
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default="default.jpg")
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)
<<<<<<< HEAD
    comments = db.relationship("Comment", backref="commenter", lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
=======

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config["SECRET_KEY"], expires_sec)
>>>>>>> app_instances
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
<<<<<<< HEAD
        s = Serializer(app.config["SECRET_KEY"])
=======
        s = Serializer(current_app.config["SECRET_KEY"])
>>>>>>> app_instances
        try:
            user_id = s.loads(token)["user_id"]
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
<<<<<<< HEAD
    comments = db.relationship("Comment", backref="article", lazy=True)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(100), nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"Comment('{self.body}', '{self.timestamp}' by user {self.user_id})"
=======

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"
>>>>>>> app_instances
