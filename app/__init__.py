
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import (
    SECRET_KEY, SQLALCHEMY_DATABASE_URI, UPLOAD_FOLDER
)


my_app = Flask(__name__)

my_app.config["SECRET_KEY"] = SECRET_KEY
my_app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
my_app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

db = SQLAlchemy(my_app)
