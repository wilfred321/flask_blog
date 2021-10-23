from flask import Blueprint
from flask import render_template, url_for, flash, redirect, request, abort
from flask_blog import db
from flask_blog.models import Post, Comment
from flask_login import current_user, login_required
from flask_blog.posts.forms import CommentForm, PostForm

posts = Blueprint("posts", __name__)


@posts.route("/post/new-post", methods=["GET", "POST"])
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            title=form.title.data, content=form.content.data, author=current_user
        )
        db.session.add(post)
        db.session.commit()
        flash("Your post has been submitted!", "success")
        return redirect(url_for("main.home"))
    return render_template(
        "create_post.html", title="New Post", form=form, legend="Create Post"
    )


@posts.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post.html", title=post.title, post=post)


@posts.route("/post/<int:post_id>/update", methods=["GET", "POST"])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author.username != current_user.username:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been updated", "success")
        return redirect(url_for("posts.post", post_id=post.id))

    if request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template(
        "create_post.html", title="Update Post", form=form, legend="Update Post"
    )


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(404)
    db.session.delete(post)
    db.session.commit()
    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))


@posts.route("/post/<int:post_id>/comment", methods=["GET", "POST"])
def comment(post_id):
    # first retrieve the post
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if request.method == "POST":
        user_id = current_user.id

        if form.validate_on_submit:
            comment = Comment(body=form.body.data, post_id=post.id, user_id=user_id)
            db.session.add(comment)
            db.session.commit()
            flash("You replied to this post", "success")
    return redirect(url_for("posts.post", post=post))
