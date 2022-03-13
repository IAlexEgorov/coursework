from traceback import print_tb
from flask import Flask, render_template, request
import requests 
import sqlite3
import subprocess

#class UserLogin:
#    def fromDB(self, user_id, db):
#        self.__user = db.getUser(user_id)
#        return self
#
#    def is_authenticated():
#        return True 
#    
#    def is_activ():
#        return True
#
#    def is_anonymous(self):
#        return False
#
#    def get_id(self):
#        return str(self.__user['id'])

app = Flask(__name__)

#def connect_db():
#    sqlite_connection = sqlite3.connect(app.config['DATABASE'])
#    sqlite_connection.row_factory = sqlite3.Row
#    return sqlite_connection

#def create_db():


#login_manager = LoginManager(app)

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

def makeStand():
    req=''''''

@app.route('/')
def index():
    return render_template('index.html', desc="Создание автостендов для разработчиков и тестеровщиков")

@app.route('/', methods=["POST", "GET"])
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