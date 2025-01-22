
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
# from flask_wtf.csrf import CSRFProtect


from config import (
    SECRET_KEY, SQLALCHEMY_DATABASE_URI, UPLOAD_FOLDER
)

# extensions
db = SQLAlchemy()
login_manager = LoginManager()
# csrf = CSRFProtect()


def create_app():
    # main app
    app = Flask(__name__)

    # configuration
    app.config["SECRET_KEY"] = SECRET_KEY
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

    # extensions
    db.init_app(app)
    login_manager.init_app(app)
    # csrf.init_app(app)

    # some settings
    login_manager.login_view = "login"

    return app


app = create_app()
