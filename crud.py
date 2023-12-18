"""Crud operations"""

from model import db, User, Movie, Rating, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    return user

def get_users():
    return User.query.all()

def create_movie(title, overview, release_date, poster_path):
    """Create and return a new movie."""
    movie = Movie(title=title,overview=overview,release_date=release_date,poster_path=poster_path)

    return movie

def get_movies():
    return Movie.query.all()

def create_rating(score,movie,user):
    rating = Rating(score=score,movie=movie,user=user)

    return rating

def get_movie_by_id(movie_id):
    movie = Movie.query.get(movie_id)
    return movie



if __name__ == '__main__':
    from server import app
    connect_to_db(app)