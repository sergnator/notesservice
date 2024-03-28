from flask import Flask, render_template

app = Flask(__name__)


@app.route("/login")
def login():
    return render_template("login.html", title="Login")


@app.route("/register")
def registration():
    return render_template("registration.html", title="Register")


@app.route("/")
@app.route("/index")
def index():
    return render_template("base.html", title="Home")


app.run()
