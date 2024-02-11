
import os
from fake_pinterest.models import User, Picture
from fake_pinterest import app, database, bcrypt
from flask import redirect, render_template, url_for
from flask_login import current_user, login_required, login_user, logout_user
from fake_pinterest.forms import FormLogin, FormCreateUser, FormPicture
from werkzeug.utils import secure_filename


@app.route("/", methods=["GET", "POST"])
def home():
    form_login = FormLogin()
    if form_login.validate_on_submit():
        user = User.query.filter_by(email=form_login.email.data).first()
        if user and user.canLogin(form_login.pwd.data):
            login_user(user, remember=True)
            return redirect(url_for("feed"))

    return render_template("home.html", form=form_login)


@app.route("/create-user", methods=["GET", "POST"])
def create_user():
    form_create_user = FormCreateUser()

    if form_create_user.validate_on_submit():
        pwd = bcrypt.generate_password_hash(form_create_user.pwd.data).decode("utf-8")
        user = User(username=form_create_user.username.data,
                    pwd=pwd,
                    email=form_create_user.email.data)

        database.session.add(user)
        database.session.commit()

        login_user(user, remember=True)
        return redirect(url_for("perfil", user_id=user.id))

    return render_template("create_user.html", form=form_create_user)


@app.route("/perfil/<user_id>", methods=["GET", "POST"])
@login_required
def perfil(user_id):
    
    if int(user_id) == int(current_user.id):
        form_picture = FormPicture()
        if form_picture.validate_on_submit():
            file = form_picture.picture.data
            sec_file_name = secure_filename(file.filename)

            # save file
            path = os.path.join(app.root_path, app.config["UPLOAD_FOLDER"], sec_file_name)
            file.save(path)

            # register to db
            picture = Picture(image=sec_file_name, user_id=int(user_id))
            database.session.add(picture)
            database.session.commit()

        return render_template(
            "perfil.html",
            user=current_user,
            form=form_picture
        )
    else:
        user = User.query.get(int(user_id))
        return render_template(
            "perfil.html",
            user=user,
            form=None
        )


@app.route("/logout")
@login_required
def logout(user="None"):
    logout_user()
    return redirect(url_for("home"))

@app.route("/feed")
@login_required
def feed():
    pics = Picture.query.order_by(Picture.cre_date.desc()).all()
    return render_template(
        "feed.html",
        pics=pics
    )
