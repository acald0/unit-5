"""Server for movie ratings app."""

from flask import Flask, render_template, request, flash, session, redirect
from model import connect_to_db, db
import crud
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined

@app.route("/")
def homepage():
    return render_template("homepage.html")

@app.route("/movies")
def all_movies():
    movies = crud.get_movies()
    return render_template("all_movies.html", movies=movies)

@app.route("/movies/<movie_id>")
def movie(movie_id):
    movie = crud.get_movie_by_id(movie_id)
    return render_template("movie_details.html", movie=movie)

@app.route("/users")
def all_users():
    users = crud.get_users()
    return render_template("all_users.html",users=users)

@app.route("/users/<user_id>")
def user(user_id):
    user = crud.get_user_by_id(user_id)
    return render_template("user_details.html", user=user)

@app.route("/users", methods=["POST"])
def register_user():
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("User with email already exists, try again with a different email!")
    else:
        user = crud.create_user(email,password)
        db.session.add(user)
        db.session.commit()
        flash("Account successfully created, please log in!")
    return redirect("/")

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user.password == password:
        session["primary_key"] = user.user_id
        flash("Logged in!")
    else:
        flash("Incorrect credentials, please try again!")
    return redirect("/")

@app.route("/rating/<movie_id>", methods=["POST"])
def rating(movie_id):
    score = request.form.get("rating")
    movie = crud.get_movie_by_id(movie_id)
    user = crud.get_user_by_id(session["primary_key"])

    new_rating = crud.create_rating(score=score,movie=movie,user=user)
    db.session.add(new_rating)
    db.session.commit()
     
    return redirect("/movies")


if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)
