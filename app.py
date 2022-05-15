from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlalchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///autostands.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    env = db.Column(db.String(15), nullable=False)
    repo = db.Column(db.String(200), nullable=False)
    branch = db.Column(db.String(20), nullable=False)
    path = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        return self.env

@app.route("/", methods=["GET", "POST"])
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
    return render_template("login.html")

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)