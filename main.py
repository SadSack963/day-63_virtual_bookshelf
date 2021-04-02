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


# ROUTES
# ======

@app.route('/')
def home():
    # Get a list of all books in the database
    all_books = db.session.query(Books).all()
    return render_template('index.html', books=all_books)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == 'POST':
        # Get data from the "name" parameters in the form <input> fields
        # Create a new book object and store it in the database file
        db.session.add(
            Books(
                title=request.form['title'],
                author=request.form['author'],
                rating=request.form['rating']
            )
        )
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add.html')


@app.route("/edit", methods=["GET", "POST"])
def edit_rating():
    if request.method == 'POST':
        # Get data from the "name" parameters in the form <input> fields and update the rating
        Books.query.get(request.form['book_id']).rating = request.form['new_rating']
        db.session.commit()
        return redirect(url_for('home'))
    # Get book_id from the argument in the <a> tag and find the book in the database
    book = Books.query.get(request.args.get('book_id'))
    return render_template('edit_rating.html', book=book)


@app.route("/delete")
def delete_book():
    # Get book_id from the argument in the <a> tag, find the book in the database and delete it
    db.session.delete(Books.query.get(request.args.get('book_id')))
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(host='localhost', port=5004, debug=False)
    pass
