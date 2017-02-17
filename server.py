"""Stars"""

from jinja2 import StrictUndefined
import calculations as c
from helpers import create_list_of_stars
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
    except sqlalchemy.orm.exc.NoResultFound:
        star = None
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

        # We need to add to the session and commit
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
                           stars=star_dict)


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
    return "Succesfully added star"


@app.route('/star_data.json/<direction>')
def create_stars_json(direction):
    """ Take the user selected direction and return json file of stars."""

    star_data = create_list_of_stars(direction)

    return json.dumps(star_data)


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

    lat = request.args.get("latitude")
    lon = request.args.get("longitude")
    date = request.args.get("date")

    if lat:
        latit = c.convert_degrees_to_radians(lat)
        session["lat"] = latit
    else:
        lat = 37.7749295
        session["lat"] = 0.65929689448
    if lon:
        longi = c.convert_degrees_to_radians(lon)
        session["lon"] = longi
    else:
        lon = -122.4194155
        session["lon"] = -2.1366218688

    if date:
        date = str(date)

        dt_object = datetime.strptime(date, '%Y-%m-%dT%H:%M')
        zone = tzwhere.tzwhere().tzNameAt(float(lat), float(lon))
        local_tz = pytz.timezone(zone)
        dttz_object = local_tz.localize(dt_object, is_dst=None)
        dt_utc = dttz_object.astimezone(pytz.utc)
        session["time"] = dt_utc
    else:
        if "time" in session:
            del session["time"]

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
