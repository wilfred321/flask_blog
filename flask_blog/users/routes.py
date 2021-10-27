import pickle
from pathlib import Path

from flask_blog.users.forms import (
    PasscodeForm,
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
    RequestResetForm,
    ResetPasswordForm,
)
from flask_blog.models import Post, User

# from flask_blog import logging

from flask_login import current_user, login_required, logout_user, login_user
from flask_blog.users.utils import (
    save_picture,
    send_reset_email,
    send_account_created_email,
    send_passcode,
    generate_passcode,
)
from flask_blog.admin.utils import save_user_json, save_user


from flask_blog import db, bcrypt, mail, oauth
from flask import Blueprint, render_template, redirect, flash, url_for, request, session

import flask_blog

users = Blueprint("users", __name__)


google = oauth.register(
    name="google",
    client_id="88130896554-jgfjq4g536lerid3l3or0mpu306k30ou.apps.googleusercontent.com",
    client_secret="FU84RphdKR-A_IwpT5MPRoss",
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    client_kwargs={"scope": "openid profile email"},
)

new_passcode = generate_passcode()

# set txt filename to write to
registered_filename_txt = "./flask_blog/static/users_records/registered_users.txt"
registered_filename_json = "./flask_blog/static/users_records/registered_users.json"


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user = User(
            username=form.username.data, email=form.email.data, password=hashed_password
        )
        db.session.add(user)
        db.session.commit()

        save_user(registered_filename_txt, user)
        save_user_json(registered_filename_json, user)
        send_account_created_email(user)
        flash(
            "Your account has been created! Please confirm and proceed to login.",
            "success",
        )

        return render_template(
            "register_success.html",
            title="Register_success",
            email=form.email.data,
        )
    return render_template("register.html", title="Register", form=form)


@users.route("/register_success")
def register_success():
    title = "Register Success"

    return render_template("register_success.html", title=title)


@users.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("main.home"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        user_email = user.email

        if user and bcrypt.check_password_hash(user.password, form.password.data):

            return redirect(url_for("users.passcode", user_email=user_email))

        flash(
            "Login Unsuccessful, Please ensure you enter the correct username and password!",
            "danger",
        )
    return render_template("login.html", title="Login", form=form)


# GOOGLE OAUTH LOGIN


@users.route("/login/passcode/<user_email>", methods=["GET", "POST"])
def passcode(user_email):

    # send mail containing passcode

    form = PasscodeForm()

    # numbers = string.digits
    # passcode = "".join(random.choice(numbers) for i in range(6))
    send_passcode(user_email, new_passcode)

    if form.validate_on_submit():
        # Generate passcode

        # user = User.query.filter_by(email=).first()

        if form.passcode.data == new_passcode:
            # print(form.passcode.data)
            # flash("passcode is correct", "success")
            user = User.query.filter_by(email=user_email).first()
            login_user(user)
            next_page = request.args.get("next")
            flash("You have been logged in ", "success")
            return redirect(next_page) if next_page else redirect(url_for("main.home"))

        else:
            flash(
                f"passcode is incorrect {new_passcode}, {form.passcode.data}", "danger"
            )

    return render_template("login_passcode.html", title="Enter Passcode", form=form)


@users.route("/google_redirect")
def google_redirect():
    google = oauth.create_client("google")
    redirect_uri = url_for("users.authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@users.route("/google_login")
def google_login():

    saved_email = session["email"]
    if not User.query.filter_by(email=saved_email).first():
        flash(
            "Login Unsuccessful, Please check your google address and login again!",
            "danger",
        )
        return redirect(url_for("users.login"))
    else:

        user = User.query.filter_by(email=saved_email).first()
        login_user(user)
        next_page = request.args.get("next")
        flash("You have been logged in", "success")
        return redirect(next_page) if next_page else redirect(url_for("main.home"))


@users.route("/authorize")
def authorize():
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    resp = google.get("userinfo")
    user_info = resp.json()
    # do something with the token and user_info
    session["email"] = user_info["email"]
    return redirect("/google_login")


# @users.route("/protected_area")
# def protected_area():

#     return f"Hello World {session['email']}"


@users.route("/logout")
def logout():
    logout_user()
    session.clear()
    flash("You have successfully logged out.", "success")
    return redirect(url_for("main.home"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account was updated successfully!", "success")
        return redirect(url_for("users.account"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="profile_pics/" + current_user.image_file)
    return render_template(
        "account.html", title="Account", image_file=image_file, form=form
    )


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = (
        Post.query.filter_by(author=user)
        .order_by(Post.date_posted.desc())
        .paginate(page=page, per_page=5)
    )
    return render_template("user_posts.html", posts=posts, user=user)


# def send_reset_email(user):
#     token = user.get_reset_token()
#     msg = Message(
#         "Password Reset Request", sender="noreply@demo.com", recipients=[user.email]
#     )

#     msg.body = f""" To reset your password, visit the following link:
# {url_for('reset_token', token = token, _external=True)}
# If you did not make this request then simply ignore this email.
# """
#     mail.send(msg)


@users.route("/reset_password", methods=["GET", "POST"])
def request_reset():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset password!", "info")
        return redirect(url_for("users.login"))
    return render_template("request_reset.html", title="Reset Password", form=form)


@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    user = User.verify_reset_token(token)

    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for("users.reset_request"))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode(
            "utf-8"
        )
        user.password = hashed_password
        db.session.commit()
        flash("Your account has been Updated! You are now able to login", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)
