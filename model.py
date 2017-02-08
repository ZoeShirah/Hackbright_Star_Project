"""models and functions for stars database"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Star(db.Model):
    """A star"""

    __tablename__ = "stars"

    star_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    ra = db.Column(db.Numeric(14, 10), nullable=False)
    dec = db.Column(db.Numeric(14, 10), nullable=False)
    name = db.Column(db.String(40))
    distance = db.Column(db.Numeric(20, 9))
    magnitude = db.Column(db.Numeric(7, 4))
    color_index = db.Column(db.Numeric(6, 4))

    def __repr__(self):
        return "<star_id = %d ra = %.4f dec = %.4f>" % (int(self.star_id), float(self.ra), float(self.dec))


class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(40))

    def __repr__(self):
        return "<user_id = %d username = %s>" % (self.user_id, self.username)


class UserStars(db.Model):
    """Stars marked and saved by a user"""

    ustar_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    star_id = db.Column(db.Integer, db.ForeignKey('stars.star_id'))

    def __repr__(self):
        return "user-star_id = %d user_id = %d star_id = %d" % (self.ustar_id, self.user_id, self.star_id)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///stars'
    app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will
    # leave you in a state of being able to work with the database
    # directly.

    from server import app
    connect_to_db(app)

    # Create our tables
    db.create_all()

    print "Connected to DB."
