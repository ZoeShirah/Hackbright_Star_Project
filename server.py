"""Stars"""

from jinja2 import StrictUndefined

from flask import Flask, jsonify, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

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
def star_list(last=0):
    """Show list of stars, 1000 at a time (there are 87,353 stars)"""
    try:
        last = int(request.args.get("last"))-1
    except TypeError:
        last = 0

    stars = Star.query.order_by(Star.star_id).offset(last).limit(1000).all()
    last = last + 1001

    return render_template("star_list.html", stars=stars, last=last)


@app.route("/stars/<star_id>")
def show_star(star_id):
    """Show info about a star"""
    star = Star.query.filter_by(star_id=star_id).one()
    return render_template("star_info.html",
                           star=star)


@app.route("/login")
def login_form():
    """Show user log in form"""
    if session.get('logged_in') is True:
        flash('user already signed in')
        return redirect('/')
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_process():
    """Process Log-in, checking password"""
    username = request.form.get('username')
    password = request.form.get('password')

    try:
        user = User.query.filter_by(username=username).one()
        if password == user.password:
            pass   # login -- for clairty in code
        else:
            flash("Wrong Password")
            return redirect('/login')

    except sqlalchemy.orm.exc.NoResultFound:
        flash("%s not found, please try again or register a new account" % (username))
        return redirect('/login')

    user_id = user.user_id
    session['user_id'] = user_id
    session['logged_in'] = True
    print(session)
    flash("Logged In")
    return redirect("/users/" + str(user_id))
    return render_template("users.html")


@app.route("/generator")
def generator_form():
    """Show generated map and form"""
    return render_template("generator.html")


@app.route("/register")
def register_form():

    if session.get('logged_in') is True:
        flash('user already signed in')
        return redirect('/')
    else:
        return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_process():

    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('e-mail')

    try:
        user = User.query.filter_by(username=username).one()
        flash('User already exists, please sign in or use another email')
        return redirect('/register')

    except sqlalchemy.orm.exc.NoResultFound:
        user = User(username=username,
                    password=password,
                    email=email)

        # We need to add to the session and commit
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user.user_id
    session['logged_in'] = True
    print(session)
    flash("Logged In")
    return redirect("/")


@app.route('/logout')
def logout_process():
    if session.get('logged_in') is True:
        del session['user_id']
        del session['logged_in']
        flash('logged out')
    else:
        flash('not logged in')

    return redirect('/login')


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show info about a user"""
    user = User.query.filter_by(user_id=user_id).one()
    return render_template("user_info.html",
                           user=user)


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

# SELECT name FROM stars WHERE name ~ '[A-Za-z]';
