from flask import Flask, render_template, redirect
from flask_login import LoginManager
from api import *
from forms import LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mega_secret_key'
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return get_name(user_id)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect("/")
    return render_template("login.html", title="Login", form=form)


@app.route("/register")
def registration():
    return render_template("registration.html", title="Register")


@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html", title="Home")


app.run()
