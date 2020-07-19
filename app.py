from flask import Flask, render_template, request,\
    redirect, url_for, session, flash, g
from flask_sqlalchemy import SQLAlchemy
from functools import wraps
# import sqlite3

app = Flask(__name__)

app.secret_key = 'my key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///posts.db"

# Create SqlAlchemy object

db = SQLAlchemy(app)

from models import *

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to logging in first!')
            return redirect(url_for('login'))
    return wrap

@app.route('/')
@app.route('/home')
@login_required
def home():
    # # g is object flask for temp request
    # g.db = connect_db()
    # cur = g.db.execute("select * from posts")
    # posts = [dict(title=row[1], description=row[2]) for row in cur.fetchall()]
    # g.db.close()
    posts = BlogPost.query.all()
    return render_template("index.html", title="Home", posts=posts)

@app.route('/welcome')
def welcome():
    return render_template("welcome.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'logged_in' in session:
        return redirect(url_for('home'))
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invlaid credentials. Please try again'
        else :
            session['logged_in'] = True
            flash('You were just logged in!')
            return redirect(url_for('home'))

    return render_template('login.html', title="Login", error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    # session.clear()
    flash('You were just logged out!')
    return redirect(url_for('welcome'))

# def connect_db():
#     return(sqlite3.connect("posts.db"))

if __name__ == '__main__':
    app.run(debug=True)
