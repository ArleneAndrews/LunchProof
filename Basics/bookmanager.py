import os

from flask import Flask, render_template, request, redirect, url_for, session, flash

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "bookdatabase.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
app.secret_key = "Fox&Dragon"

db = SQLAlchemy(app)

class Book(db.Model):
    title = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    writer = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        bookInfo = "<Title: {}>".format(self.title), "<Author: {}>".format(self.writer)
        return bookInfo

@app.route("/", methods=["GET", "POST"])
def home():
    books = None
    if request.form:
        try:
            book = Book(
                title=request.form.get("title"),
                writer=request.form.get("writer"))
            db.session.add(book)
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
def logout():
    session.pop('logged_in', None)
    flash('You are now logged out. Thanks for reading!')
    return redirect(url_for('welcome'))
  
if __name__ == "__main__":
    app.run(debug=True)