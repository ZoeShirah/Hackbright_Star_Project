"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

import decimal

from flask_sqlalchemy import SQLAlchemy
import sqlalchemy

from model import Star, User, UserStars, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC123"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""
    return render_template("homepage.html")


@app.route("/stars")
def user_list():
    """Show list of stars."""

    stars = Star.query.all()
    return render_template("star_list.html", stars=stars)


# @app.route("/stars/<star_id>")
# def show_user(user_id):

#     user_object = User.query.filter_by(user_id=user_id).one()
#     rating_objects = Rating.query.filter_by(user_id=user_id).all()
#     movie_ratings = {}

#     for rating_object in rating_objects:
#         movie_object = Movie.query.filter_by(movie_id=rating_object.movie_id).one()
#         movie_ratings[movie_object.movie_id] = {'score': rating_object.score,
#                                                 'title': movie_object.title}

#     return render_template("user_info.html",
#                            user=user_object,
#                            movie_ratings=movie_ratings)

@app.route("/login")
def login_form():
    """Show user log in form"""
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_process():
    """Show user log in form"""
    return render_template("users.html")


@app.route("/generator")
def generator_form():
    """Show generated map and form"""
    return render_template("generator.html")

# SELECT name FROM stars WHERE name ~ '[A-Za-z]';

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the
    # point that we invoke the DebugToolbarExtension
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(port=5000, host='0.0.0.0')
