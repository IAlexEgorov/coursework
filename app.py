from traceback import print_tb
from flask import Flask, render_template, request
import requests 
import sqlite3
import subprocess
from flask import Flask, render_template, request, redirect, url_for
import flask_login

app = Flask(__name__)
app.secret_key = 'my_secret'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

def checkUser(login, password):
    req='''ldapsearch 
    -h ipa.web-bee.loc -p 389 
    -b uid='''+login+''',cn=users,cn=accounts,dc=web-bee,dc=loc 
    -D uid='''+login+''',cn=users,cn=accounts,dc=web-bee,dc=loc -w '''+password
    sub=subprocess.call(req.split())
    if (sub==0):
        return True
    else:
        return False

class User(flask_login.UserMixin):
    pass

@login_manager.user_loader
def user_loader(email):
    #if email not in users:
    #    return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    #if email not in users:
    #    return

    user = User()
    user.id = email
    return user


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return '''
               <form action='login' method='POST'>
                <input type='text' name='email' id='email' placeholder='email'/>
                <input type='password' name='password' id='password' placeholder='password'/>
                <input type='submit' name='submit'/>
               </form>
               '''
    email = request.form['email']
    if request.form['password'] == users[email]['password']:
        user = User()
        user.id = email
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
        if checkUser(login, password):

            return render_template('index.html', desc="Успешно")
        else:
            return render_template('index.html', desc="Ошибка доступа")

if __name__=="__main__":
    app.run(debug=True)