
from flask import render_template, redirect, flash

from app import my_app, db
from app.models import (User, Post, Comment)
from app.forms import PostForm


@my_app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)


@my_app.route("/create_post", methods=["GET", "POST"])
def post():
    form = PostForm()
    if form.validate_on_submit():
        new_post = Post(title=form.title.data, content=form.content.data, user_id=1)
        db.session.add(new_post)
        db.session.commit()
        flash("Post added Successfully")
        return redirect("/")

    return render_template("make_post.html", form=form)


@my_app.route("/delete_post_<int:post_id>")
def remove_post(post_id):
    selected_post = Post.query.get(post_id)
    print(Post.query)
    print("===")
    print(Post.query.get(post_id))
    db.session.delete(selected_post)
    db.session.commit()
    return redirect("/")