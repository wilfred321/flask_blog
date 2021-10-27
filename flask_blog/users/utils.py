import os
import secrets
import random, string
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flask_blog import mail, oauth


# RESIZE AND SAVE PICTURE


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/profile_pics/", picture_fn
    )
    # form_picture.save(picture_path)

    i = Image.open(form_picture)
    output_size = (125, 125)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


# SEND RESET EMAIL


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(
        "Password Reset Request", sender="noreply@demo.com", recipients=[user.email]
    )
    msg.body = f""" To reset your password, visit the following link:
{url_for('users.reset_token', token = token, _external=True)}
If you did not make this request then simply ignore this email.
"""
    mail.send(msg)


# send account_creation_email
def send_account_created_email(user):
    msg = Message(
        "Confirm your Account",
        sender="noreply@demo.com",
        recipients=[user.email],
    )
    msg.body = f"""Account has been created for {user.email} """
    mail.send(msg)


def generate_passcode():
    numbers = string.digits
    passcode = "".join(random.choice(numbers) for i in range(6))
    return passcode


def send_passcode(user_email, passcode):
    msg = Message(
        "Confirm Login",
        sender="noreply@demo.com",
        recipients=[user_email],
    )
    msg.body = f"Your passcode is:  {passcode}"
    mail.send(msg)




    # Path(filename).write_text(data)


# REGISTER APP FOR OAUTH


# @current_app.route("/reset_password", methods=["GET", "POST"])
# def request_reset():
#     if current_user.is_authenticated:
#         return redirect(url_for("main.home"))
#     form = RequestResetForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(email=form.email.data).first()
#         send_reset_email(user)
#         flash("An email has been sent with instructions to reset password!", "info")
#         return redirect(url_for("users.login"))
#     return render_template("request_reset.html", title="Reset Password", form=form)


# @current_app.route("/reset_password/<token>", methods=["GET", "POST"])
# def reset_token(token):
#     if current_user.is_authenticated:
#         return redirect(url_for("main.home"))
#     user = User.verify_reset_token(token)

#     if user is None:
#         flash("That is an invalid or expired token", "warning")
#         return redirect(url_for("users.reset_request"))
#     form = ResetPasswordForm()
#     if form.validate_on_submit():
#         hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
#             "utf-8"
#         )
#         user.password = hashed_password
#         db.session.commit()
#         flash("Your account has been Updated! You are now able to login", "success")
#         return redirect(url_for("users.login"))
#     return render_template("reset_token.html", title="Reset Password", form=form)
