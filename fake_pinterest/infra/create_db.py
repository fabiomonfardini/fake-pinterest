from fake_pinterest import app
from fake_pinterest import database
from fake_pinterest.models import User, Picture

with app.app_context():
    database.create_all()