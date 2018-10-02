import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "spotdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Spot(db.Model):
    place = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
   
    def __repr__(self):
        return "<Name: {}>".format(self.place)

@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        venue = Spot(place=request.form.get("venue"))
        db.session.add(venue)
        db.session.commit()
    spots = Spot.query.all()
    return render_template("index.html", spots=spots)

@app.route("/update", methods=["POST"])
def update():
    newname = request.form.get("newname")
    oldname = request.form.get("oldname")
    venue = Spot.query.filter_by(place=oldname).first()
    Spot.venue = newname
    db.session.commit()
    return redirect("/")
  
if __name__ == "__main__":
    app.run(debug=True)