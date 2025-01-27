
from app import app, db
from app.models import (User, Post, Comment)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        # db.session.commit()

        db.session.add(User(username="nika",
                            email="n@n.n",
                            role="admin",
                            password_hash="scrypt:32768:8:1$1TC25QbeXlvm8jEe$5f42936f5c5ac3f31badc69b0da298f5365a39a1d0daecd0a6e1c7d7fc8c27992bb756cfc487607f82120078c606bf7fba1353088efd3e526da6c5f5ecd45136"))
        db.session.add(Post(title="initPostTitle",
                            content="this is post... there is big text!",
                            user_id="1"))
        db.session.add(Comment(content="i liked this post!",
                               user_id="1", post_id=1))
        db.session.commit()
