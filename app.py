
import json
from flask import Flask, render_template, request, redirect
import requests
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    poster = db.Column(db.String(100), nullable=False)

    def __rep__(self):
        return '<Movie %r>' % self.id


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)

    def __rep__(self):
        return '<Book %r>' % self.id


class Series(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    poster = db.Column(db.String(100), nullable=False)

    def __rep__(self):
        return '<Series %r>' % self.id


@app.route('/', methods=['POST', 'GET'])
def home():
    response = requests.get("https://zenquotes.io/api/today")
    quote_json = response.json()
    quote = quote_json[0]['q']
    author = quote_json[0]['a']
    return render_template("index.html", quote=quote, author=author)


@app.route('/movies', methods=['POST', 'GET'])
def movies():
    if request.method == 'POST':
        movie_name = request.form['content']
        response = requests.get(
            f"https://www.omdbapi.com/?t={movie_name}&apikey=a2cef660")
        data = response.json()
        if(data["Response"]) == "False":
            return 'Serie not Found'
        new_movie = Movie(content=data["Title"],
                          genre=data["Genre"], year=data["Year"], poster=data["Poster"])

        try:
            db.session.add(new_movie)
            db.session.commit()
            return redirect('/movies')
        except:
            return 'There was an error while adding the movie'

    else:
        movies = Movie.query.all()
        return render_template("movies.html", movies=movies)


@app.route('/books', methods=['POST', 'GET'])
def books():
    if request.method == 'POST':
        book_name = request.form['content']
        new_book = Book(content=book_name)

        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect('/books')
        except:
            return 'There was an error while adding the book'

    else:
        books = Book.query.all()
        return render_template("books.html", books=books)


@app.route('/series', methods=['POST', 'GET'])
def series():
    if request.method == 'POST':
        serie_name = request.form['content']
        response = requests.get(
            f"https://www.omdbapi.com/?t={serie_name}&apikey=a2cef660")
        data = response.json()
        if(data["Response"]) == "False":
            return 'Serie not Found'
        new_series = Series(content=data["Title"],
                            genre=data["Genre"], year=data["Year"], poster=data["Poster"])

        try:
            db.session.add(new_series)
            db.session.commit()
            return redirect('/series')
        except:
            return 'There was an error while adding the serie'

    else:
        series = Series.query.all()
        return render_template("series.html", series=series)


@app.route('/deleteMovie/<int:id>')
def deleteMovie(id):
    movie_to_delete = Movie.query.get_or_404(id)
    try:
        db.session.delete(movie_to_delete)
        db.session.commit()
        return redirect('/movies')
    except:
        return 'There was an error while deleting that movie'


@app.route('/deleteSerie/<int:id>')
def deleteSerie(id):
    serie_to_delete = Series.query.get_or_404(id)
    try:
        db.session.delete(serie_to_delete)
        db.session.commit()
        return redirect('/series')
    except:
        return 'There was an error while deleting that serie'


@app.route('/deleteBook/<int:id>')
def deleteBook(id):
    book_to_delete = Book.query.get_or_404(id)
    try:
        db.session.delete(book_to_delete)
        db.session.commit()
        return redirect('/books')
    except:
        return 'There was an error while deleting that book'


if __name__ == "__main__":
    app.run(debug=True)
