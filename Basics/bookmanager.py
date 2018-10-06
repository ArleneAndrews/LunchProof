import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    writer = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        bookInfo = "<Title: {}>".format(self.title), "<Author: {}>".format(self.writer)
        return bookInfo

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

@app.route("/", methods=["GET", "POST"])
def home():
    books = None
    if request.form:
        try:
            book = Book(
                title=request.form.get("title"),
                writer=request.form.get("writer"))
            db.session.add(book)
            # db.session.add(writer)
            db.session.commit()
        except Exception as e:
            print("Failed to add book")
            print(e)
    book = Book.query.all()
    return render_template("index.html", books=book)

@app.route("/update", methods=["POST"])
def update():
    try:
            newtitle = request.form.get("newtitle")
            oldtitle = request.form.get("oldtitle")
            book = Book.query.filter_by(title=oldtitle).first()
            book.title = newtitle
            db.session.commit()
    except Exception as e:
        print("Couldn't update book title")
        print(e)
    return redirect("/")

@app.route("/updatea", methods=["POST"])
def updatea():
    try:
            newwriter = request.form.get("newwriter")
            oldwriter = request.form.get("oldwriter")
            book = Book.query.filter_by(writer=oldwriter).first()
            book.writer = newwriter
            db.session.commit()
    except Exception as e:
        print("Couldn't update book author")
        print(e)
    return redirect("/")

@app.route("/delete", methods=["POST"])
def delete():
    title = request.form.get("title")
    book = Book.query.filter_by(title=title).first()
    db.session.delete(book)
    db.session.commit()
    return redirect("/")
  
if __name__ == "__main__":
    app.run(debug=True)