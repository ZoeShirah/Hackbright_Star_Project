import calculations as c
from flask import session
from model import Star
from datetime import datetime


def create_list_of_stars(direction):
    """with direction create a list of visible stars by querying the database"""

    stars = Star.query.filter(Star.magnitude < 5).order_by(Star.star_id).all()

    star_data = []
    for star in stars:

        #ra is in hours/min/sec, 1 hour = 15 degrees, so must multiply by 15
        ra = c.convert_degrees_to_radians((15*star.ra))
        dec = c.convert_degrees_to_radians(star.dec)
        la = float(session.get("lat", 0.65929689448))
        lo = float(session.get("lon", -2.1366218688))
        t = session.get("time", datetime.utcnow())

        altAz = c.get_current_altAz(float(ra), float(dec), lo, la, t)
        visible = c.get_visible_window(altAz.alt, altAz.az)
        if direction in visible:
            star_info = c.convert_sky_to_pixel(altAz.alt, altAz.az, direction)
            color = c.get_color(float(star.color_index))
            star_info.update({'magnitude': float(star.magnitude),
                              'color': color,
                              'id': star.star_id})
            if star.name:
                star_info.update({'name': star.name})

            star_data.append(star_info)

    return star_data
