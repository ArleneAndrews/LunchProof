import os

from flask import Flask, render_template, request, redirect, url_for, session, flash, g, Response, json
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

# Used for testing and dev
from settings import key
# Used for prod
# key = os.environ.get('key')

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "spotdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

app.secret_key = key


db = SQLAlchemy(app)

# basic model for data - returns the name of the Spot
class Spot(db.Model):
    place = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    address = db.Column(db.String(80))
    phone = db.Column(db.INT)
    visit = db.Column(db.String(8))
    queue = db.Column(db.String(8))
    rating = db.Column(db.INT)
    
   
    def __repr__(self):
        return "<Name: {}>".format(self.place)

# Wrapper for login - ease of use and portability
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
                return f(*args, **kwargs)
        else:
                flash('Please log in.')
                return redirect(url_for('login'))
    return wrap

# Basic index form - showing all fields that will eventually be needed
@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    spots = None
    if request.form:
        try:
            venue = Spot(
                place = request.form.get("venue"),
                address = request.form.get("address"),
                phone = request.form.get("phone"),
                visit = request.form.get("visit"),
                queue = request.form.get("queue"),
                rating = request.form.get("rating")
            )
            db.session.add(venue)
            db.session.commit()
        except Exception as e:
            print("Failed to add spot")
            print(e)
    spots = Spot.query.all()
    return render_template("index.html", spots=spots)

# Update Individual Spot - button access
@app.route("/update", methods=["POST"])
def update():
    try:
        newname = request.form.get("newname")
        oldname = request.form.get("oldname")
        spot = Spot.query.filter_by(place=oldname).first()
        spot.place = newname
        db.session.commit()
    except Exception as e:
            print("Failed to update spot")
            print(e)
    return redirect("/")

# Delete Individual Spot - button access
@app.route("/delete", methods=["POST"])
def delete():
    place = request.form.get("place")
    spot = Spot.query.filter_by(place=place).first()
    db.session.delete(spot)
    db.session.commit()
    return redirect("/")

# Welcome Page - Currently (Nov 17) not the landing page
@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

# Login Page - Currently (Nove 17) the opening page
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST': # Fixed credentials while building
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('Welcome! You are now logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

# Logout page - only route to Welcome page currently (Nov 17)
@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out. Thanks for reading!')
    return redirect(url_for('welcome'))

# Edit method - get JSON from HTML, and triggers a DB query ERRORS
# TODO This section works, but not clearing until it all works
# TODO Needs login confirmation
@app.route('/edit', methods=['POST'])
def edit():
    if request.method == 'POST':
        place = request.get_json
        print(place)
        spot = Spot.query.filter_by(place=place).first()
    return render_template('/edit')

if __name__ == "__main__":
    app.run(debug=True)