from flask import Flask, render_template, redirect, url_for, request, make_response
from flask_login import LoginManager, current_user, logout_user, login_required
from flask_login import login_user as login_user_flask

from api import *
from forms import LoginForm, WriteNoteForm, ReadNoteForm

import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mega_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return get_name(user_id)


@app.route("/login", methods=["GET", "POST"])
def login_():
    form = LoginForm()
    if form.validate_on_submit():
        user = login({"username": form.username.data,
                      "password": form.password.data})  # обращаемся к api для проверки пользователя
        if isinstance(user, User):  # пользователь существует
            max_age = None
            if form.remember_me.data:
                max_age = datetime.timedelta(seconds=60 * 60 * 24 * 365)
            login_user_flask(user, remember=form.remember_me.data, duration=max_age)
            res = make_response(redirect(url_for('index')))
            res.set_cookie("password", form.password.data, max_age=max_age)
            return res
        return render_template("login.html", title="Login", form=form, error=user)  # выводит сообщение Api
    return render_template("login.html", title="Login", form=form, error="None")


@app.route("/register", methods=["GET", "POST"])
def registration():
    form = LoginForm()
    if form.validate_on_submit():
        user = register({"username": form.username.data, "password": form.password.data})  # создаём пользователя
        if isinstance(user, User):  # создали корректно
            max_age = None
            if form.remember_me.data:
                max_age = datetime.timedelta(seconds=60 * 60 * 24 * 365)
            login_user_flask(user, remember=form.remember_me.data, duration=max_age)
            res = make_response(redirect(url_for('index')))
            res.set_cookie("password", form.password.data, max_age=max_age)
            return res
        return render_template("registration.html", title="Register", form=form,
                               error=user)  # если не корректно, то выводит сообщение
    return render_template("registration.html", title="Register", error="None", form=form)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    form = WriteNoteForm()
    if form.validate_on_submit():
        note = {"content": form.content.data, "private": form.is_private.data}
        user = User.from_dict({"username": current_user.username, "password": request.cookies.get("password")})
        res = create_note(note, user)  # создаём заметку
        if not isinstance(res, Note):
            return render_template("create.html", title="Create Note", form=form,
                                   error=res)  # выводим сообщение об ошибке
    return render_template("create.html", title="Create", form=form, error="None")


@app.route("/read", methods=["GET", "POST"])
def read():
    form = ReadNoteForm()
    if form.validate_on_submit():
        res = get_note_by_id(form.search_field.data)
        if isinstance(res, Note):
            return render_template("read.html", title="Read Note", form=form, text=res.content, error="None")
        return render_template("read.html", title="Read Note", form=form, error=res)
    return render_template("read.html", title="Read Note", form=form, error="None", text="")


@app.route("/logout")
@login_required
def logout_():
    logout_user()
    res = make_response(redirect(url_for('index')))
    res.set_cookie("password", "", max_age=0)
    return res


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("base.html", title="Home", current_user=current_user)


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login_'))

    return response


app.run(port=8000)
