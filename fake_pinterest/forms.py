from flask_wtf import FlaskForm
from wtforms import FileField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from fake_pinterest.models import User

class FormLogin(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    pwd = PasswordField("Password", validators=[DataRequired()])
    login_button = SubmitField("Login")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError("E-mail or password are incorrect.")

class FormCreateUser(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    pwd = PasswordField("Password", validators=[DataRequired(), Length(6, 20)])
    pwd_confirmation = PasswordField("Confirm your password", validators=[DataRequired(), EqualTo("pwd")])
    submit_button = SubmitField("Submit")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email already registered. Please, do login to continue.")
        
class FormPicture(FlaskForm):
    picture = FileField("Picture", validators=[DataRequired()])
    upload_button = SubmitField("Upload")