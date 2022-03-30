from flask import Flask, render_template, request, redirect, url_for, flash, g
import flask_login
from ldap3 import Connection, Server, Entry
import os
import sqlite3

LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASSWORD = os.getenv("LDAP_PASSWORD")


# Конфигурация 
DATABASE = "/tmp/flsite.db"
DEBUG = True
SECRET_KEY = "jlkvlvbreoqefvb"

app = Flask(__name__)
app.secret_key = "my_secret"
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path,"flsite.db")))

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


class User(flask_login.UserMixin):
    pass


def connect_db():
    conn = sqlite3.connect(app.config["DATABASE"])
    conn.row_factory = sqlite3.Row
    return conn

def create_db():
    db = connect_db()
    with app.open_resource("sq_db.sql", mode="r") as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()

def get_db():
    if not hasattr(g, "link_db"):
        g.link_db = connect_db()
    return g.link_db

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@login_manager.user_loader
def user_loader(login):
    print("load user")
    
    if login not in users:
        return

    user = User()
    user.id = login
    return user


@login_manager.request_loader
def request_loader(request):
    login = request.form.get("login")
    if login not in users:
        return

    user = User()
    user.id = login
    return user


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return """
               <form action='login' method='POST'>
                <input type='text' name='login' id='login' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               """
    login = request.form["login"]
    password = request.form["password"]
    if check_user_from_ldap_from_ldap(login, password):
        user = User()
        user.id = login
        flask_login.login_user(user)
        return redirect(url_for("index"))
    return "Bad login"


# Добавить страницу для неавторизованных
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for("login"))


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return "Logged out"


@app.route("/")
@flask_login.login_required
def index():
    return render_template("index.html")


@app.route("/", methods=["POST", "GET"])
@flask_login.login_required
def contact():
    if request.method == "POST":
        print(request.form)
        login = request.form["login"]
        password = request.form["pass"]
        
        if check_user_from_ldap_from_ldap(login, password):
            flash("Успешно")
        else:
            flash("Ошибка доступа")
        return render_template("index.html")


if __name__ == "__main__":
    create_db() 
    app.run(debug=True)
