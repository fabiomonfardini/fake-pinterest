from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///community.db"
app.config["SECRET_KEY"] = "b04875baae27745923126151c1d90e82"
app.config["UPLOAD_FOLDER"] = "static/posted_pics"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = "home" # type: ignore

