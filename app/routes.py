
from flask import render_template

from app import my_app
from app.models import (User, Post, Comment)


@my_app.route("/")
def index():
    posts = Post.query.all()
    return render_template("index.html", posts=posts)
