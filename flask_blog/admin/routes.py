from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, current_app
from flask_blog import db
from flask_blog.models import User, Post
from flask_blog.admin.utils import save_user_json, save_user, extract_users
from run import app


admin = Blueprint("admin", __name__)


deleted_filename_txt = app.Config["DELETED_TXT"]
deleted_filename_json = app.Config["DELETED_JSON"]


@admin.route("/admin", methods=["GET", "POST"])
def admin():

    if request.method == "GET":
        users = User.query.all()
        deleted_user = request.args.get("deleted_user")
        # user = session.get("user")
        if deleted_user != None:

            # flash(
            #     f"User with username {user.username} was deleted successfully",
            #     "success",
            # )
            return render_template(
                "admin.html",
                title="admin-interface",
                users=users,
                deleted_user=deleted_user,
            )

        else:

            # logging.info(user_id)
            return render_template("admin.html", title="admin-interface", users=users)

    # else:
    #     request.method = "POST"
    #     user_id = request.args.get("user_id")
    #     return f"<h1>User id is: {user_id}</h1>"


@admin.route("/admin_delete_user", methods=["GET", "POST"])
def admin_delete_user():
    if request.method == "POST":
        user_id = request.form.get("selected_user")

        # session["user_id"] = user_id
        user = User.query.filter_by(id=user_id).first()
        username = user.username
        db.session.delete(user)
        db.session.commit()

        save_user(deleted_filename_txt, user)
        save_user_json(deleted_filename_json, user)
        flash(f"User {username} deleted successfully", "success")

    return redirect(url_for("users.admin", deleted_user=username))


@admin.route("/display", methods=["GET", "POST"])
def display():

    if request.method == "POST":
        user_type = request.form.get("selected_user")
        if user_type == "registered_users":
            registered_users = extract_users(registered_filename_json)

            return render_template("admin.html", registered_users=registered_users)

        elif user_type == "deleted_users":

            deleted_users = extract_users(deleted_filename_json)
            return render_template("admin.html", deleted_users=deleted_users)

            #     user_info = {}
            #     for user in deleted_users:

            #         data = user.split(",")
            # return f""" ('username: {data[0]}')
            # ('email: {data[1]}')
            # 'data_posted: {data[2]}')"""

            # data = f.split("\n")

            # for item in data:
            #     print(item)
            # data.strip()

            # user_info["username"] = data[0]
            # user_info["email"] = data[1]
            # user_info["data_deleted"] = data[2]
            # user_info["time_deleted"] = data[3]

            # print(f"<h1>{(deleted_users)}</h1>")
            # return "<h1>Selected user is Deleted User</h1>"

        else:
            return "user type is none of the above"

    return render_template("admin.html", title="admin-interface")

    # user_id = request.args.get("user_id")
    # return a dictionary containing the username information

    return "Noting was returned"


@admin.route("/admin/tag_user", methods=["GET", "POST"])
def tag_user_post():
    if request.method == "POST":
        user_id = request.form.get("selected_user")
        user = User.query.get_or_404(user_id)
        posts = Post.query.filter_by(user_id=user_id)
    return render_template("admin.html", posts=posts, user=user)
