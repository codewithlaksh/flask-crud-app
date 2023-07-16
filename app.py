from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dotenv import load_dotenv
import os

# Load all the variables inside the .env file
load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
db = SQLAlchemy(app)
app.app_context().push()

class Todos(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), nullable=False)
    body = db.Column(db.String(800), nullable=False)
    created = db.Column(db.DateTime(), default=datetime.now())

    def __repr__(self):
        return f'{self.title} - {self.created}'

    def __init__(self, title, body):
        self.title = title
        self.body = body

@app.route("/")
def home():
    todos = Todos.query.all()
    return render_template("index.html", todos=todos)

@app.route("/edit/<int:pk>", methods=["GET", "POST"])
def edit(pk):
    todo = Todos.query.filter_by(sno=pk).first()
    if request.method == "POST":
        title = request.form.get('title')
        body = request.form.get('desc')

        todo.title = title
        todo.body = body
        db.session.commit()
        flash('Your to-do has been updated!', 'success')
        return redirect(url_for('home'))
    return render_template("edit.html", todo=todo)

@app.route("/delete/<int:pk>", methods=["GET", "POST"])
def delete(pk):
    todo = Todos.query.filter_by(sno=pk).first()
    if request.method == "POST":
        db.session.delete(todo)
        db.session.commit()
        flash('Your to-do has been deleted!', 'success')
        return redirect(url_for('home'))
    return render_template("delete.html", todo=todo)

@app.route("/add", methods=["POST"])
def add():
    title = request.form.get('title')
    body = request.form.get('desc')

    todo = Todos(title, body)
    db.session.add(todo)
    db.session.commit()
    flash('Your to-do has been created!', 'success')
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True, port=8080, host='0.0.0.0')
