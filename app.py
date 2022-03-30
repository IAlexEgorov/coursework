from flask import Flask, render_template, request, redirect, url_for, flash, g
import flask_login
import os
import sqlite3
from fdata import FDataBase

LDAP_USER = os.getenv("LDAP_USER")
LDAP_PASSWORD = os.getenv("LDAP_PASSWORD")


# Configuration
DATABASE = "/tmp/flsite.db"
DEBUG = True
SECRET_KEY = "jlkvlvbreoqefvb"

app = Flask(__name__)
app.config.from_object(__name__)

app.config.update(dict(DATABASE=os.path.join(app.root_path,'flsite.db')))


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


# App functions 
@app.route("/")
def index():
    db = get_db()
    dbase = FDataBase(db)
    db_user=dbase.getUserName(username="alex.e")
    return render_template("index.html", user=db_user)


@app.route("/", methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        print(request.form)
        login = request.form["login"]
        password = request.form["pass"]
        return render_template("index.html")

    
@app.route("/login", methods=["POST", "GET"])
def login():
    return render_template("login.html")


@app.route("/logout", methods=["POST", "GET"])
def logout():
    return render_template("index.html")



if __name__ == "__main__":
    #create_db()
    app.run(debug=True)
