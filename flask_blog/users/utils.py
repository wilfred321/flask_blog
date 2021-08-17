import os
import secrets
from PIL import Image
from flask import url_for
from flask_mail import Message
from flask_blog import app, mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, "static/profile_pics/", picture_fn)
    # form_picture.save(picture_path)

    i = Image.open(form_picture)
    output_size = (125, 125)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request", sender="noreply@demo.com", recipients=[user.email]
    )
    msg.body = f""" To reset your password, visit the following link:
{url_for('reset_token', token = token, _external=True)}
If you did not make this request then simply ignore this email.    
"""
    mail.send(msg)


@app.route("/reset_password", methods=["GET", "POST"])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset password!", "info")
        return redirect(url_for("login"))
    return render_template("request_reset.html", title="Reset Password", form=form)


@app.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    user = User.verify_reset_token(token)

    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash("Your account has been Updated! You are now able to login", "success")
        return redirect(url_for("login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
