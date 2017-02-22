import calculations as c
from model import Star, User, UserStar, db
from sqlalchemy.orm.exc import NoResultFound
import generator_helpers as g


def make_user(username, password, email):
    try:
        user = User.query.filter_by(username=username).one()
        return None
    except NoResultFound:
        user = User(username=username,
                    password=password,
                    email=email)

        #add to the session and commit
        db.session.add(user)
        db.session.commit()
        return user


def get_star_info(star_id):
    try:
        star = Star.query.filter_by(star_id=star_id).one()
        consts = g.get_list_of_constellations(star_id)
        for i in range(len(consts)):
            consts[i] = c.replace_constellation_name(consts[i])
    except NoResultFound:
        star = None
        consts = []
    return [star, consts]


def get_userStar_dict(user_id):
    userStars = UserStar.query.filter_by(user_id=user_id).all()

    star_dict = {}
    for userStar in userStars:
        UStar = Star.query.filter_by(star_id=userStar.star_id).one()
        star_dict[UStar.star_id] = {'ra': UStar.ra, 'dec': UStar.dec}
        if UStar.name.strip():
            star_name = UStar.name
            star_dict[UStar.star_id].update({'name': star_name})
    return star_dict


def find_star(term):
    try:
        search_id = term[:8]
        search_star = int(search_id)
    except ValueError:
        search_star = term
    if type(search_star) == int:
        return "/stars/" + term[:8]
    else:
        search_star = search_star.lower().capitalize()
        try:
            star = Star.query.filter_by(name=search_star).one()
            return "/stars/" + str(star.star_id)
        except NoResultFound:
            return None


def validate_login(username, password):
    try:
        user = User.query.filter_by(username=username).one()
    except NoResultFound:
        return str(username) + " not found, please try again or register a new account"

    if password != user.password:
        return "Wrong password"

    return user


def save_a_star(star_id, user_id):
    try:
        userStars = UserStar.query.filter_by(user_id=user_id).filter_by(star_id=star_id).one()
        return "You have already saved this star!"
    except NoResultFound:
        userStars = UserStar(user_id=user_id,
                             star_id=star_id)
        # add to the session and commit
        db.session.add(userStars)
        db.session.commit()
    return "Star Added!"
