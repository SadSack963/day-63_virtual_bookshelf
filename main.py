from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


# Create the database file in /database/new-books-collection.db
FILE_URL = 'sqlite:///database/new-books-collection.db'

# Create the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = FILE_URL  # load the configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Significant overhead if True. Future default: False
db = SQLAlchemy(app)  # create the SQLAlchemy object by passing it the application


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float(), unique=False, nullable=False)

    def __repr__(self):
        return f'<Book: {self.title}>'


# Create the database file and tables
# This code must come _after_ the class definition
if not os.path.isfile(FILE_URL):
    db.create_all()


def db_new_book(title, author, rating):
    # Create a book and store it in the database file
    book = Books(title=title, author=author, rating=rating)
    print(book)
    db.session.add(book)
    db.session.commit()


@app.route('/')
def home():
    # Get a list of all books in the database
    all_books = db.session.query(Books).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        rating = request.form['rating']
        db_new_book(title=title, author=author, rating=rating)
        return redirect(url_for('home'))
    return render_template('add.html')


if __name__ == "__main__":
    app.run(host='localhost', port=5004, debug=False)
    pass
