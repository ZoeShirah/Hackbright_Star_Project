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

# SELECT name FROM stars WHERE name ~ '[A-Za-z]';
