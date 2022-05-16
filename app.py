from flask import Flask, redirect, render_template, request, url_for, flash
from flask_login import UserMixin, LoginManager, login_user, login_required
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy
from werkzeug.security import check_password_hash, generate_password_hash


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///autostands.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'super secret key'
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    env = db.Column(db.String(15), nullable=False)
    repo = db.Column(db.String(200), nullable=False)
    branch = db.Column(db.String(20), nullable=False)
    path = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return self.env


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    login = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "POST":
        env = request.form["env"]
        repo = request.form["repo"]
        branch = request.form["branch"]
        path = request.form["path"]

        item = Item(env=env, repo=repo, branch=branch, path=path)

        try:
            db.session.add(item)
            db.session.commit()
            return redirect("/")
        except:
            return "Ошибка"
    else:
        items = Item.query.order_by(Item.env).all()
        stands_count = len(items)
        return render_template("index.html", data=items, stands_count=stands_count)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        login = request.form.get('login')
        password = request.form.get('password')
        user = User.query.filter_by(login=login).first()
        print(user)
        if not user or not check_password_hash(user.password, password):
            flash('Check your login or password')
            return redirect(url_for('login'))
        login_user(user) 
        return redirect(url_for('index'))
    else:
        return render_template("login.html")


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)