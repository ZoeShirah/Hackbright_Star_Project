"""Utility file to seed stars database from hygfull in seed_data/"""

from sqlalchemy import func
from sqlalchemy.exc import DataError
from model import Star, User, UserStar

from model import connect_to_db, db
from server import app


def load_stars():
    """Load stars from hygfull.csv into database."""

    print "Stars"

    # Delete all rows in table, so if we need to run this a second time,
    # we won't be trying to add duplicate users
    Star.query.delete()

    # Read u.user file and insert data
    f = open("seed_data/hygfull.csv")
    next(f) # skip first row
    for row in f:
        row = row.rstrip()
        StarID, Hip, HD, HR, Gliese, BayerFlamsteed, ProperName, RA, Dec, Distance, Mag, AbsMag, Spectrum, ColorIndex = row.split(",")

        try:
            float(ColorIndex)
        except ValueError:
            ColorIndex = 0

        star = Star(star_id=StarID,
                    name=ProperName,
                    ra=RA,
                    dec=Dec,
                    distance=Distance,
                    magnitude=Mag,
                    color_index=ColorIndex)

        # We need to add to the session and commit our work
        db.session.add(star)

    db.session.commit()
      
    f.close()


# def set_val_user_id():
#     """Set value for the next user_id after seeding database"""

#     # Get the Max user_id in the database
#     result = db.session.query(func.max(User.user_id)).one()
#     max_id = int(result[0])

#     # Set the value for the next user_id to be max_id + 1
#     query = "SELECT setval('users_user_id_seq', :new_id)"
#     db.session.execute(query, {'new_id': max_id + 1})
#     db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    # In case tables haven't been created, create them
    db.create_all()

    # Import different types of data
    load_stars()
    #set_val_user_id()
