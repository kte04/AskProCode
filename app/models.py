
from app import db, my_app
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(16), nullable=False, default="")

    def __init__(self, username, email, password_hash):
        self.username = username
        self.email = email
        self.password_hash = password_hash

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User {self.username}>"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __repr__(self):
        return f"<Post {self.title}>"


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    user = db.relationship('User', backref=db.backref('comments', lazy=True))
    post = db.relationship('Post', backref=db.backref('comments', lazy=True))

    def __repr__(self):
        return f"<Comment {self.content[:20]}>"


if __name__ == "__main__":
    with my_app.app_context():
        db.create_all()
        db.session.add(User(username="nika",
                            email="n@n.n",
                            password_hash="scrypt:32768:8:1$1TC25QbeXlvm8jEe$5f42936f5c5ac3f31badc69b0da298f5365a39a1d0daecd0a6e1c7d7fc8c27992bb756cfc487607f82120078c606bf7fba1353088efd3e526da6c5f5ecd45136"))
        db.session.add(Post(title="initPostTitle",
                            content="this is post... there is big text!",
                            user_id="1"))
        db.session.add(Comment(content="i liked this post!",
                               user_id=1, post_id=1))
        db.session.commit()
