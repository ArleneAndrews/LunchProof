import os

from flask import Flask
from flask import render_template
from flask import request

from flask_sqlalchemy import SQLAlchemy, Model # added to avid conflicts in the future

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "spotdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Spot(db.Model):
    name = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    addy = db.Column(db.String(80), unique=True, nullable=False)
    notes = db.Column(db.String(250), unique=False, nullable=True)

    def __repr__(self):
        return "<Name: {}>".format(self.name)

@app.route("/", methods=["GET", "POST"])
def home():
   if request.form:
        spot = Spot(name=request.form.get("name"))
        db.session.add(spot)
        db.session.commit()
    return render_template("index.html")
  
if __name__ == "__main__":
    app.run(debug=True)