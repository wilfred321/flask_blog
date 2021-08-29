from datetime import datetime

from sqlalchemy.orm import backref
from sqlalchemy.sql.schema import ForeignKey
from flask_blog import db, login_manager, app
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(), unique=True, nullable=False)
    image_file = db.Column(db.String(100), nullable=False, default="default.jpg")
    password = db.Column(db.String(100), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)
    comments = db.relationship("Comment", backref="commenter", lazy=True)
    liked = db.relationship("PostLike", backref="user", lazy="dynamic")

    # like and unlike methods
    def like_post(self, post):
        if not self.has_liked_post(post):
            like = PostLike(user_id=self.id, post_id=post.id)
            db.session.add(like)

    def unlike_post(self, post):
        if self.has_liked_post(post):
            PostLike.query.filter_by(post_id=post.id, user_id=self.id).delete()

    def has_liked_post(self, post):
        return (
            PostLike.query.filter(
                PostLike.user_id == self.id, PostLike.post_id == post.id
            ).count()
            > 0
        )

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config["SECRET_KEY"], expires_sec)
        return s.dumps({"user_id": self.id}).decode("utf-8")

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config["SECRET_KEY"])
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
    comments = db.relationship("Comment", backref="article", lazy="dynamic")
    likes = db.relationship("PostLike", backref="post", lazy="dynamic")

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


class PostLike(db.Model):
    __tablename__ = "post_like"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
