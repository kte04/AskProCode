
from flask import render_template, redirect, flash, request, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import sqlalchemy

from app import app, db, login_manager
from app.models import (User, Post, Comment)
from app.forms import (PostForm, RegistrationForm, LoginForm)


# def search_user_by(**kwargs):


@app.route("/")
def index():
    return render_template("index.html", current_user=current_user)


@app.route("/feed")
@login_required
def feed():
    posts = Post.query.all()


# @app.route("/")
# def index():
#     posts = Post.query.all()
#     return render_template("index.html", posts=posts, current_user=current_user)


@app.route("/create_post", methods=["GET", "POST"])
@login_required
def post():
    form = PostForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_post = Post(title=form.title.data,
                            content=form.content.data,
                            user_id=current_user.id)
            db.session.add(new_post)
            db.session.commit()
            flash("Post added Successfully")
            return redirect("/")
        else:
            flash("Invalid fields.")

    return render_template("make_post.html", form=form, current_user=current_user)


@app.route("/delete_post_<int:post_id>")
@login_required
def remove_post(post_id):
    selected_post = Post.query.get(post_id)

    # print(Post.query.get(post_id))  # remove this
    # print(f"admin: {current_user.is_admin()}")
    # print(f"is_owner: {current_user.is_owner(selected_post)}")
    if current_user.is_admin() or current_user.is_owner(selected_post):
        db.session.delete(selected_post)
    try:
        db.session.commit()
    except sqlalchemy.exc.IntegrityError as e:
        flash(f"Error: {repr(e)}. redirecting to Home")
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if request.method == "POST":
        if form.validate_on_submit():
            username = form.username.data
            print(f"username={username}")
            found_user = User.query.filter_by(username=username).first()
            print(f"found: {found_user}")
            if found_user is None:
                new_user = User(
                    username=username,
                    email=form.email.data,
                    password_hash=generate_password_hash(form.password.data),
                    role="user")
                db.session.add(new_user)
                db.session.commit()
                flash("You successfully registered")
                return redirect("/")
            else:
                # username already exists
                flash(f"Username \"{found_user.username}\" already exists.")
                return redirect("/register")
        else:
            flash("Input is not valid. Errors:")
            for error_k, error_v in form.errors:
                # XXX i do not if this syntax is always.
                # for example:
                # form.errors = {'email': ['Invalid email address.'],}
                flash(f"error: {error_k}: {error_v}")

    return render_template("register.html", form=form, current_user=current_user)


@app.route("/list_users")
def list_users():
    users = User.query.all()
    return render_template("list_users.html", users=users, current_user=current_user)


@app.route("/delete_user_<int:user_id>")
def remove_user(user_id):
    selected_user = User.query.get(user_id)
    if selected_user is None:
        flash(f"User with id={user_id} not found!")
        return redirect("/list_users")
    else:
        db.session.delete(selected_user)
        db.session.commit()
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and check_password_hash(user.password_hash, form.password.data):
                flash("Logged in succesfully!")
                login_user(user=user)
                return redirect(request.args.get("next") or "/profile")
            else:
                for e in form.errors:
                    flash(e)

    return render_template("login.html", form=form, current_user=current_user)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.")
    return redirect('/')


# Route for the current user's profile
@app.route("/profile")
@login_required
def view_profile():
    posts = [post for post in Post.query.all() if post.user.id == current_user.id]
    return render_template("profile.html", user=current_user, current_user=current_user, posts=posts)


# Route for viewing another user's profile by username
@app.route("/profile/<string:username>")
@login_required
def view_profile_by_username(username):
    user = User.query.filter_by(username=username).first()
    print(user)
    if user is None:
        flash(f"Username {username} does not exist.", "danger")
        return redirect("/profile")  # Redirect to the current user's profile
    return render_template('profile.html', user=user, current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)
