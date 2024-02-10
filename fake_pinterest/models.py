
from fake_pinterest import database, login_manager, bcrypt
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(database.Model, UserMixin):
    id = database.schema.Column(database.Integer, primary_key=True)
    username = database.Column(database.String, nullable=False)
    email = database.Column(database.String, nullable=False, unique=True)
    pwd = database.Column(database.String, nullable=False)
    cre_date = database.Column(database.DateTime, nullable=False, default=datetime.now)
    pics = database.relationship("Picture", backref="user", lazy=True)

    def __init__(self, username, email, pwd) -> None:
        super().__init__()
        self.username = username
        self.email = email
        self.pwd = pwd

    def canLogin(self, pwd_to_validate=""):
        valid_pwd = bcrypt.check_password_hash(self.pwd, pwd_to_validate)
        return valid_pwd

class Picture(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    image = database.Column(database.String, default="default.png")
    cre_date = database.Column(database.DateTime, nullable=False, default=datetime.now)
    user_id = database.Column(database.String, database.ForeignKey("user.id"), nullable=False)

    def __init__(self, image, user_id) -> None:
        super().__init__()
        self.image = image
        self.user_id = user_id