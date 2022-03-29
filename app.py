from flask import Flask, render_template, request, redirect, url_for
from ldap3 import Connection, Server, Entry
import flask_login
import os

app = Flask(__name__)
app.secret_key = 'my_secret'

LDAP_USER = "uid=bot.admin,cn=users,cn=accounts,dc=web-bee,dc=loc"
LDAP_PASSWORD = "DEVpassword"

login_manager = flask_login.LoginManager()
login_manager.init_app(app)
users = {'alex.e':{"password": "password"}}


def check_ldap_user(user):
    server = Server('ipa.web-bee.loc', use_ssl=True)

    conn = Connection(server, user=ldap_user, password=ldap_password, auto_bind=True)
    rez = conn.search('cn=users,cn=accounts,dc=web-bee,dc=loc', '(uid='+user+')', attributes="*")

def check_user_from_ldap_from_ldap(login, password):
    server = Server('ipa.web-bee.loc', use_ssl=True)
    conn = Connection(server, user=ldap_user, password=ldap_password, auto_bind=True)
    if conn:
        return True
    else:
        return False

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(login):
    if login not in users:
        return

    user = User()
    user.id = login
    return user

@login_manager.request_loader
def request_loader(request):
    login = request.form.get('login')
    if login not in users:
        return

    user = User()
    user.id = login
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='login' id='login' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''
    login = request.form['login']
    password = request.form['password']
    if check_user_from_ldap_from_ldap(login, password):
        user = User()
        user.id = login
        flask_login.login_user(user)
        return redirect(url_for('index'))
    return 'Bad login'


# Добавить страницу для неавторизованных 
@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('login'))


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'


@app.route('/')
@flask_login.login_required
def index():
    return render_template('index.html', desc="Создание автостендов для разработчиков и тестеровщиков")

@app.route('/', methods=["POST", "GET"])
@flask_login.login_required
def contact():
    if request.method == 'POST':
        print(request.form)
        login = request.form["login"]
        password = request.form["pass"]
        if check_user_from_ldap_from_ldap(login, password):
            return render_template('index.html', desc="Успешно")
        else:
            return render_template('index.html', desc="Ошибка доступа")

if __name__=="__main__":
    app.run(debug=True)