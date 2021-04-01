from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os


# # Manually creating database file and adding an entry
# import sqlite3
#
# db = sqlite3.connect('database/books-collection.db')  # Connection to database (create the file if it doesn't exist)
# cursor = db.cursor()  # pointer to database row
#
# # Create the database table (do this only once)
# cursor.execute(
#     "CREATE TABLE books ("
#     "id INTEGER PRIMARY KEY, "
#     "title varchar(250) NOT NULL UNIQUE, "
#     "author varchar(250) NOT NULL, "
#     "rating FLOAT NOT NULL"
#     ")"
# )
#
# # Error sqlite3.IntegrityError: UNIQUE constraint failed: books.id
# # This error occurs because the code is being run twice.
# # ===== This happens when debug=True in app.run() =====
# cursor.execute("INSERT INTO books VALUES(22, 'Harry Potter 22', 'Jay. K. Rowling', '9.5')")
# db.commit()


r"""
Database URLs
=============
https://docs.sqlalchemy.org/en/14/core/engines.html#database-urls
These URLs follow RFC-1738, and usually can include username, password, hostname, database name
  as well as optional keyword arguments for additional configuration. In some cases a file path is accepted,#
  and in others a “data source name” replaces the “host” and “database” portions.
The typical form of a database URL is:
  dialect+driver://username:password@host:port/database
Dialect names include the identifying name of the SQLAlchemy dialect, a name such as
  sqlite, mysql, postgresql, oracle, or mssql.
The drivername is the name of the DBAPI to be used to connect to the database using all lowercase letters.
  If not specified, a “default” DBAPI will be imported if available - this default is typically the most widely
  known driver available for that backend.
Special characters such as those that may be used in the password need to be URL encoded to be parsed correctly.
  The encoding for these characters can be generated using urllib.parse:
      import urllib.parse
      urllib.parse.quote_plus("kx%jj5/g")
      >>> 'kx%25jj5%2Fg'
SQLite connects to file-based databases, using the Python built-in module sqlite3 by default.

As SQLite connects to local files, the URL format is slightly different to
  PostgreSQL, MySQL, Oracle and Microsoft SQL Server.
The “file” portion of the URL is the filename of the database.
For a relative file path, this requires three slashes
  engine = create_engine('sqlite:///foo.db')
For an absolute file path, the three slashes are followed by the absolute path
  engine = create_engine('sqlite:///C:\\path\\to\\foo.db')
To use a SQLite :memory: database, specify an empty URL
  engine = create_engine('sqlite://')
"""
# Create the database file in /database/new-books-collection.db
FILE_URI = 'sqlite:///database/new-books-collection.db'


r"""
Using SQLAlchemy API
====================
https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/
https://flask-sqlalchemy.palletsprojects.com/en/2.x/api/
For the common case of having one Flask application all you have to do is to create your Flask application,
  load the configuration of choice and then create the SQLAlchemy object by passing it the application.
Once created, that object then contains all the functions and helpers from both sqlalchemy and sqlalchemy.orm.
  Furthermore it provides a class called Model that is a declarative base which can be used to declare models.
"""
# Create the Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = FILE_URI  # load the configuration
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Significant overhead if True. Future default: False
db = SQLAlchemy(app)  # create the SQLAlchemy object by passing it the application


class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), unique=False, nullable=False)
    rating = db.Column(db.Float(), unique=False, nullable=False)

    def __repr__(self):
        """
        Python __repr__() function returns the object representation in string format.\n
        This method is called when repr() function is invoked on the object.\n
        https://www.journaldev.com/22460/python-str-repr-functions\n

        :return: string
        """
        # This will allow each book object to be identified by its title when printed.
        return f'<Book: {self.title}>'


# Create the database file and tables
# This code must come _after_ the class definition
if not os.path.isfile(FILE_URI):
    db.create_all()


# Create a book and store it in the database file
book = Books(title='Harry Potter', author='J. K. Rowling', rating='9.3')
print(book.__repr__())
db.session.add(book)
db.session.commit()


# CRUD (Create, Read, Update, and Delete)


# all_books = []
#
# @app.route('/')
# def home():
#     return render_template('index.html', books=all_books)
#
#
# @app.route("/add", methods=["GET", "POST"])
# def add():
#     if request.method == 'POST':
#         title = request.form['title']
#         author = request.form['author']
#         rating = request.form['rating']
#         all_books.append({'title': title, 'author': author, 'rating': rating})
#         print(all_books)
#     return render_template('add.html')
#
#
# if __name__ == "__main__":
#     app.run(host='localhost', port=5004, debug=False)
#     pass
