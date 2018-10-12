import os

from flask import Flask, render_template, request, redirect, url_for, session, flash, g
from functools import wraps
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "spotdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

app.secret_key = "Fox&Dragon"

db = SQLAlchemy(app)

class Spot(db.Model):
    place = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    """ address = db.Column(db.String(80), unique=True, nullable=False)
    phone = db.Column(db.INT, unique=True)
    lat = db.Column(db.INT, nullable=False)
    lon = db.Column(db.INT, nullable=False)
    visited = db.Column(db.INT, unique=True, nullable=False)
    rating = db.Column(db.INT, unique=True, nullable=False)
    tags = db.Column(db.String(80), unique=True, nullable=False) """
   
    def __repr__(self):
        return "<Name: {}>".format(self.spot)

def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
                return f(*args, **kwargs)
        else:
                flash('Please log in.')
                return redirect(url_for('login'))
    return wrap

def check_admin():
    """
    prevent unauthorized changes
    """
    if not current_user.is_admin:
        abort(403)

@app.route("/", methods=["GET", "POST"])
@login_required
def home():
    spots = None
    #add_spot()
    if request.form:
        spot = Spot(place=request.form.get("spot"))
        print spot
        db.session.add(spot)
        db.session.commit()
    #add_spot()
    spots = Spot.query.all()
    return render_template("index.html", spots=spots, title="Book Tutorial Mashup")

@app.route('/spots', methods=['GET','POST'])
#@login_required
def list_spots():
    """
    list all the spots in the db
    """
    #check_admin()

    spots = Spot.query.all()
    return render_template("index.html", spots=spots, title="Spots")
    
@app.route('/add', methods=['GET', 'POST'])
@login_required
def add_spot():
    """
    add a spot into the database
    """
    #check_admin()

    add_spot = True
    # instantiate the form as a SpotForm() 

    #validate SpotForm submission
    # if form.validate_on_submit():
    #   venue = Spot(place=request.form.place.data, 
    #                   description=request.form.desc.data)
    try:
        venue = Spot(place=request.form.get("venue")
        # TODO: add stuff here
        )
        db.session.add(venue)
        db.session.commit()
        flash('Successfully added a new Spot to the list')
    except Exception as e:
        print("Failed to add spot")
        print(e)
    #return redirect(url_for('/spots'))
    return redirect(url_for('/'))
# load the spots template
#return render_template('path/to/spots.html', action="Add",
#                        add_spot=add_spot, form=form, title="Add A New Spot")

@app.route("/update/<int:id>", methods=["GET","POST"])
#@login_required
def update(id):
    """
    Create a route to display/edit spots on a page
    """
    #check_admin()
    #add_spot = False
    try:
        newname = request.form.get("newname")
        oldname = request.form.get("oldname")
        spot = Spot.query.filter_by(id=id).first()
        spot.place = newname
        db.session.commit()
        flash('You have edited a spot!')
    except Exception as e:
            print("Failed to update spot")
            print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    place = request.form.get("place")
    spot = Spot.query.filter_by(place=place).first()
    db.session.delete(spot)
    db.session.commit()
    return redirect("/")

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            flash('Welcome! You are now logged in.')
            return redirect(url_for('home'))
    return render_template('login.html', error=error)

@app.route('/logout')
@login_required
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out. Thanks for reading!')
    return redirect(url_for('welcome'))
if __name__ == "__main__":
    app.run(debug=True)