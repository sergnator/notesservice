from flask import Flask, render_template, redirect, url_for, make_response, request
from flask_login import LoginManager, current_user, logout_user, login_required
from flask_login import login_user as login_user_flask

from alice_notes.api import *
from forms import LoginForm, WriteNoteForm, ReadNoteForm, RegisterForm

import datetime
import catflask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mega_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)

app.register_blueprint(catflask.cat_blueprint)


def __login(user, form):
    if isinstance(user, User):  # пользователь существует
        max_age = None
        if form.remember_me.data:
            max_age = datetime.timedelta(seconds=60 * 60 * 24 * 365)
        login_user_flask(user, remember=form.remember_me.data, duration=max_age)
        res = make_response(redirect(url_for('index')))
        res.set_cookie("password", user.password, max_age=max_age)
        res.set_cookie("auth_token", user.auth_token, max_age=max_age)
        return res


@login_manager.user_loader
def load_user(user_id):
    return get_name(user_id)


@app.route("/login", methods=["GET", "POST"])
def login_():
    form = LoginForm()
    if form.validate_on_submit():
        user = login({"email": form.email.data,
                      "password": form.password.data})  # обращаемся к api для проверки пользователя\
        res = __login(user, form)
        if res is not None:
            return res
        return render_template("login.html", title="Register", error=user, form=form, token="")
    token = ""
    if current_user.is_authenticated:
        token = request.cookies.get(current_user.id, "")

    return render_template("login.html", title="Login", form=form, error="None", token=token)


@app.route("/register", methods=["GET", "POST"])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        user = register({"username": form.username.data, "password": form.password.data,
                         "email": form.email.data})  # создаём пользователя
        res = __login(user, form)
        if res is not None:
            return None
        return render_template("registration.html", title="Register", error=user, form=form, token="")
    token = ""
    if current_user.is_authenticated:
        token = request.cookies.get(current_user.id, "")
    return render_template("registration.html", title="Register", error="None", form=form, token=token)


@app.route("/create", methods=["GET", "POST"])
@login_required
def create():
    token = ""
    if current_user.is_authenticated:
        token = request.cookies.get(current_user.id, "")
    form = WriteNoteForm()
    if form.validate_on_submit():
        note = {"content": form.content.data, "private": form.is_private.data}
        user = User.from_dict(
            {"username": current_user.username, "password": request.cookies[str(current_user.id)],
             "email": current_user.email})
        res = create_note(note, user)  # создаём заметку
        if not isinstance(res, Note):
            return render_template("create.html", title="Create Note", form=form,
                                   error=res, value="Create", token=token)  # выводим сообщение об ошибке
        return redirect(url_for('index'))
    return render_template("create.html", title="Create", form=form, error="None", value="Create", token=token)


@app.route("/read", methods=["GET", "POST"])
def read():
    form = ReadNoteForm()
    token = ""
    if current_user.is_authenticated:
        token = request.cookies.get(current_user.id, "")
    if form.validate_on_submit():
        res = get_note_by_id(form.search_field.data)
        if isinstance(res, Note):
            return render_template("read.html", title="Read Note", form=form, text=res.content, error="None",
                                   token=token)
        return render_template("read.html", title="Read Note", form=form, error=res, token=token)
    return render_template("read.html", title="Read Note", form=form, error="None", text="", token=token)


@app.route("/logout")
@login_required
def logout_():
    logout_user()
    res = make_response(redirect(url_for('index')))
    res.set_cookie("password", "", max_age=0)
    return res


@app.route("/")
@app.route("/index")
def index():
    token = ""
    if isinstance(current_user, str):
        return render_template("base.html", title="Home", current_user=current_user, token="")
    if current_user.is_authenticated:
        token = request.cookies.get("auth_token", "")
        user = login({"email": current_user.email, "password": request.cookies.get("password")})
        notes = user.notes
        return render_template("profile.html", title="Profile", current_user=current_user, notes=notes, token=token)
    return render_template("base.html", title="Home", current_user=current_user, token="")


@app.route("/delete/<int:_id>")
@login_required
def delete_(_id):
    delete(User.from_dict(
        {"username": current_user.username, "password": request.cookies.get("password"),
         "email": current_user.email}),
        _id)
    return redirect(url_for('index'))


@app.route("/edit/<int:_id>", methods=["GET", "POST"])
@login_required
def edit_(_id):
    token = ""
    if current_user.is_authenticated:
        token = request.cookies.get(current_user.id, "")
    user = login({"email": current_user.email, "password": request.cookies.get("password")})
    form = WriteNoteForm()
    if form.validate_on_submit():
        for note in user.notes:
            if note.id == _id:
                note.content = form.content.data
                note.private = form.is_private.data
                edit_note(note, user)
                return redirect("/")
    if isinstance(user, User):
        for note in user.notes:
            if note.id == _id:
                form.content.data = note.content
                form.is_private.data = note.private
                break
        else:
            return render_template("create.html", title="Create Note", form=form, current_user=current_user,
                                   error=f"Note {_id} not found", value="Edit", token=token)
    else:
        return render_template("create.html", title="Create Note", form=form, current_user=current_user, error=user,
                               value="Edit", token=token)
    return render_template("create.html", title="Edit Note", form=form, current_user=current_user, error="None",
                           value="Edit", token=token)


@app.after_request
def redirect_to_sign(response):
    if response.status_code == 401:
        return redirect(url_for('login_'))

    return response


app.run(port=8000)
