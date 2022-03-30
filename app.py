from flask import Flask, render_template, request, redirect, url_for, flash, g
from flask_login import LoginManager, login_required, UserMixin, login_user, logout_user
import os
import sqlite3
from classes.FDataBase import FDataBase
from classes.UserLogin import UserLogin

LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASSWORD = os.getenv("LDAP_PASSWORD")


# Configuration
DATABASE = "/tmp/flsite.db"
DEBUG = True
SECRET_KEY = "jlkvlvbreoqefvb"

app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))

login_manager = LoginManager(app)

# Data Base functions 
def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def create_db():
    """Вспомогательная функция для создания таблиц БД"""
    db = connect_db()
    with app.open_resource('sq_db.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()
    db.close()


def get_db():
    '''Соединение с БД, если оно еще не установлено'''
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.teardown_appcontext
def close_db(error):
    '''Закрываем соединение с БД, если оно было установлено'''
    if hasattr(g, 'link_db'):
        g.link_db.close()



# Login functions 
class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(login):
    db = connect_db()
    fdb = FDataBase(db)
    if not fdb.getUser(login):
        return
    user = User()
    user.id = login
    return user


@login_manager.request_loader
def request_loader(request):
    db = connect_db()
    fdb = FDataBase(db)
    login = request.form.get('login')
    password = request.form.get('password')
    if not fdb.checkUser(login, password):
        return
    user = User()
    user.id = login
    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template("login.html")

# App functions 
@app.route("/", methods=["POST", "GET"])
@app.route("/index", methods=["POST", "GET"])
@login_required
def index():
    if request.method == "POST":
        print(request.form)
        return render_template("index.html")
    return render_template("index.html")

    
@app.route("/login", methods=["POST", "GET"])
def login():
    db = get_db()
    fdb = FDataBase(db)
    if request.method == 'GET':
        return render_template("login.html")

    login = request.form.get('login')
    password = request.form.get('password')
    if fdb.checkUser(login, password):
        user = User()
        user.id = login
        login_user(user)
        flash('Успешный вход', category='success')
        return redirect(url_for('index'))
    flash('Неверные данные', category='error')
    return render_template("login.html")


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    return render_template("login.html")



if __name__ == "__main__":
    #create_db()
    app.run(debug=True)