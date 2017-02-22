"""Stars"""

import os
from jinja2 import StrictUndefined
import calculations as c
from helpers import create_list_of_stars, create_list_of_constellations, get_list_of_constellations, replace_constellation_name
from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension
import json
import sqlalchemy
from datetime import datetime
import pytz
from tzwhere import tzwhere
from model import Star, User, UserStar, connect_to_db, db


app = Flask(__name__)
# Required to use Flask sessions and the debug toolbar
app.secret_key = "Polaris8222"
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

    try:
        star = Star.query.filter_by(star_id=star_id).one()
        consts = get_list_of_constellations(star_id)
        for i in range(len(consts)):
            consts[i] = replace_constellation_name(consts[i])
    except sqlalchemy.orm.exc.NoResultFound:
        star = None
        consts = []
    return render_template("star_info.html",
                           star=star,
                           constellations=consts)


@app.route("/login")
def login_form():
    """Show user log in form"""

    if session.get('user_id'):
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
    if user.lat is not None:
        session["d_lat"] = user.lat
        session["lat"] = c.convert_degrees_to_radians(user.lat)
        session["d_lon"] = user.lon
        session["lon"] = c.convert_degrees_to_radians(user.lon)
    flash("Logged In")
    return redirect("/users/" + str(user_id))
    return render_template("users.html")


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

    try:
        user = User.query.filter_by(username=username).one()
        flash('User already exists, please sign in or use another email')
        return redirect('/register')

    except sqlalchemy.orm.exc.NoResultFound:
        user = User(username=username,
                    password=password,
                    email=email)

        #add to the session and commit
        db.session.add(user)
        db.session.commit()

    session['user_id'] = user.user_id
    print(session)
    flash("Logged In")
    return redirect("/")


@app.route('/logout')
def logout_process():
    """logout the user by removing their info from the session"""

    if 'user_id' in session:
        del session['user_id']
        flash('logged out')
    else:
        flash('not logged in')

    return redirect('/login')


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show info about a user"""

    user = User.query.filter_by(user_id=user_id).one()
    userStars = UserStar.query.filter_by(user_id=user_id).all()

    star_dict = {}
    for userStar in userStars:
        UStar = Star.query.filter_by(star_id=userStar.star_id).one()
        star_dict[UStar.star_id] = {'ra': UStar.ra, 'dec': UStar.dec}
        if UStar.name.strip():
            star_name = UStar.name
            star_dict[UStar.star_id].update({'name': star_name})

    return render_template("user_info.html",
                           user=user,
                           stars=star_dict,
                           secret=SECRET)


@app.route("/set_user_location")
def set_user_location():
    user_id = session.get("user_id")
    lat = request.args.get("lat")
    lon = request.args.get("lng")
    user = User.query.filter_by(user_id=user_id).one()
    user.lat = lat
    user.lon = lon
    db.session.commit()

    lat = c.convert_degrees_to_radians(lat)
    session["lat"] = lat
    session["d_lat"] = float(lat)

    lon = c.convert_degrees_to_radians(lon)
    session["lon"] = lon
    session["d_lon"] = float(lon)

    return redirect("/users/"+str(user_id))


@app.route("/add_to_saved/<star_id>")
def add_to_saved(star_id):
    """Add a star to the user's list of saved stars"""

    user_id = session.get('user_id')

    try:
        userStars = UserStar.query.filter_by(user_id=user_id).filter_by(star_id=star_id).one()
        return "You have already saved this star!"
    except sqlalchemy.orm.exc.NoResultFound:
        userStars = UserStar(user_id=user_id,
                             star_id=star_id)

        # add to the session and commit
        db.session.add(userStars)
        db.session.commit()
    return "Star Added!"


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


@app.route('/search')
def search():
    """Search for a star by name or star id"""

    term = request.args.get("name")
    try:
        search_id = term[:8]
        search_star = int(search_id)
    except ValueError:
        search_star = term

    if type(search_star) == int:
        return redirect("/stars/" + term[:8])
    else:
        search_star = search_star.lower().capitalize()
        try:
            star = Star.query.filter_by(name=search_star).one()
            return redirect("/stars/" + str(star.star_id))
        except sqlalchemy.orm.exc.NoResultFound:
            flash("no star with that name in this database")
            return redirect("/stars")


@app.route('/change_defaults')
def change_defaults():
    """ Take user input for lat/long and time and redraw sky"""

    lat = request.args.get("lat")
    lon = request.args.get("lng")
    date = request.args.get("date")

    if lat:
        latit = c.convert_degrees_to_radians(lat)
        session["lat"] = latit
        session["d_lat"] = float(lat)

    if lon:
        longi = c.convert_degrees_to_radians(lon)
        session["lon"] = longi
        session["d_lon"] = float(lon)

    if date:
        date = str(date)

        dt_object = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        zone = tzwhere.tzwhere().tzNameAt(float(lat), float(lon))
        local_tz = pytz.timezone(zone)
        dttz_object = local_tz.localize(dt_object, is_dst=None)
        dt_utc = dttz_object.astimezone(pytz.utc)
        session["time"] = dt_utc

    return redirect('/generator')


@app.route('/clear')
def clearSession():
    if "lat" in session:
        del session["lat"]
        del session["d_lat"]
    if "lon" in session:
        del session["lon"]
        del session["d_lon"]
    if "time" in session:
        del session["time"]
    if session['user_id']:
        user = User.query.filter_by(user_id=session['user_id']).one()
        session["d_lat"] = user.lat
        session["lat"] = c.convert_degrees_to_radians(user.lat)
        session["d_lon"] = user.lon
        session["lon"] = c.convert_degrees_to_radians(user.lon)

    return redirect('/generator')


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
