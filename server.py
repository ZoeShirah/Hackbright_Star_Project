"""Stars"""

from datetime import datetime
import os
from jinja2 import StrictUndefined
from flask import Flask, render_template, redirect, request, flash, session
# from flask_debugtoolbar import DebugToolbarExtension
import json
from model import Star, User, connect_to_db, db
#helper files
import calculations as c
from generator_helpers import create_list_of_stars, create_list_of_constellations, get_planet_info
from helpers import get_star_info, make_user, get_userStar_dict
from helpers import find_star, validate_login, save_a_star

app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = os.environ['FLASK_SECRET']
# So that if you use an undefined variable in Jinja2, it raises an error.
app.jinja_env.undefined = StrictUndefined
SECRET = os.environ['GOOGLE_API_KEY']


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

    star, consts = get_star_info(star_id)

    return render_template("star_info.html",
                           star=star,
                           constellations=consts)


@app.route("/login")
def login_form():
    """Show user log in form"""

    if 'user_id' in session:
        flash('user already signed in')
        return redirect('/')
    else:
        return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_process():
    """Process Log-in, checking password"""

    username = request.form.get('username')
    password = request.form.get('password')

    message = validate_login(username, password)
    if type(message) is str:
        flash(message)
        return redirect("/login")
    else:
        user = message
        flash(("%s Logged In!") % (username))
        session['user_id'] = user.user_id
        if user.lat is not None:
            update_session(user.lat, user.lon)

    return redirect("/users/" + str(user.user_id))


@app.route("/generator")
def generator_form():
    """Show generated map and form"""

    return render_template("generator.html", secret=SECRET)


@app.route("/register")
def register_form():
    """show the registration form"""

    if 'user_id' in session:
        flash('user already signed in')
        return redirect('/')
    else:
        return render_template("register_form.html")


@app.route("/register", methods=["POST"])
def register_process():
    """Add the user to the database and log them in"""

    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('e-mail')

    user = make_user(username, password, email)
    if user is None:
        flash('User already exists, please choose a different username or sign in')
        return redirect('/register')

    session['user_id'] = user.user_id
    flash("Logged In")
    return redirect("/")


@app.route('/logout')
def logout_process():
    """logout the user by removing their info from the session"""

    if 'user_id' in session:
        del session['user_id']
        clearSession()
        flash('logged out')
    else:
        flash('not logged in')

    return redirect('/login')


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show info about a user"""

    user = User.query.filter_by(user_id=user_id).one()
    star_dict = get_userStar_dict(user_id)

    return render_template("user_info.html",
                           user=user,
                           stars=star_dict,
                           secret=SECRET)


@app.route("/set_user_location")
def set_user_location():
    """get the user's location and add it to the database as their defualt"""
    user_id = session.get("user_id")
    lat = request.args.get("lat")
    lon = request.args.get("lng")

    user = User.query.filter_by(user_id=user_id).one()
    user.lat = lat
    user.lon = lon
    db.session.commit()

    update_session(lat, lon)

    return redirect("/users/"+str(user_id))


@app.route("/add_to_saved/<star_id>")
def add_to_saved(star_id):
    """Add a star to the user's list of saved stars"""

    user_id = session.get('user_id')

    return save_a_star(star_id, user_id)


@app.route('/star_data.json/<direction>')
def create_stars_json(direction):
    """ Take the user selected direction and return json file of stars."""

    star_data = create_list_of_stars(direction)

    return json.dumps(star_data)


@app.route('/constellation_data.json/<direction>')
def create_constellation_json(direction):
    """ Take the user selected direction and returns constellations."""

    star_data = create_list_of_stars(direction)
    constellation_data = create_list_of_constellations(star_data, direction)

    return json.dumps(constellation_data)


@app.route('/planet_data.json/<direction>')
def create_planet_json(direction):
    """ Take the user selected direction and returns visible planets."""

    lat = session.get("lat",  0.6592968944837353)
    lon = session.get("lon", -2.1366218688419805)
    time = session.get("time", datetime.utcnow())

    planet_data = get_planet_info(time, lat, lon, direction)
    return json.dumps(planet_data)


@app.route('/search')
def search():
    """Search for a star by name or star id"""

    term = request.args.get("name")
    url = find_star(term)
    if url:
        return redirect(url)
    else:
        flash("no star with that name in this database")
        return redirect("/stars")


@app.route('/change_defaults')
def change_defaults():
    """ Take user input for lat/long and time and redraw sky"""

    lat = request.args.get("lat")
    lon = request.args.get("lng")
    date = request.args.get("date")

    if lat and lon:
        update_session(lat, lon)
    else:
        lat = session.get("d_lat", 37.7887459)
        lon = session.get("d_lon", -122.41158519999999)

    if date:
        dt_utc = c.get_utc_time(date, lat, lon)
        session["time"] = dt_utc

    return redirect('/generator')


@app.route('/clear')
def clear():
    """Clear the time and location info, if user is logged in reset to thier defaults"""

    clearSession()
    if 'user_id' in session:
        user = User.query.filter_by(user_id=session['user_id']).one()
        update_session(user.lat, user.lon)

    return redirect('/generator')


def clearSession():
    """clear time and location info from the session"""
    if "lat" in session:
        del session["lat"]
        del session["d_lat"]
    if "lon" in session:
        del session["lon"]
        del session["d_lon"]
    if "time" in session:
        del session["time"]


def update_session(lat=None, lon=None):
    if lat:
        r_lat = c.convert_degrees_to_radians(lat)
        session["lat"] = r_lat
        session["d_lat"] = float(lat)

    if lon:
        r_lon = c.convert_degrees_to_radians(lon)
        session["lon"] = r_lon
        session["d_lon"] = float(lon)

if __name__ == "__main__":  # pragma: no cover

    # while developing/debugging *********
    # app.debug = True
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # app.jinja_env.auto_reload = app.debug  # make sure templates, etc. are not cached in debug mode
    #***********************************

    connect_to_db(app, os.environ.get("DATABASE_URL", "postgresql:///stars"))

    db.create_all(app=app)
    PORT = int(os.environ.get("PORT", 5000))

    #while developing/debugging ****************
    # app.run(host="0.0.0.0", port=PORT)
    # #***********************************

    #for deployment on heroku ***********
    DEBUG = "NO_DEBUG" not in os.environ
    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
    #********************************
