import calculations as c
from flask import session
from model import Star, Const_Line, Constellation
from datetime import datetime


def get_altaz(star):
    """Get the Altitude and Azimuth of a star given the star object.

    Lat/Long and Time are from the flask session, or the default if the user
    has not entered any.
    """

    #ra is in hours/min/sec, 1 hour = 15 degrees, so must multiply by 15
    ra = c.convert_degrees_to_radians((15*star.ra))
    dec = c.convert_degrees_to_radians(star.dec)
    la = float(session.get("lat", 0.65929689448))
    lo = float(session.get("lon", -2.1366218688))
    t = session.get("time", datetime.utcnow())

    return c.get_current_altAz(float(ra), float(dec), lo, la, t)


def create_list_of_stars(direction):
    """with direction create a list of visible stars by querying the database"""

    stars = Star.query.filter(Star.magnitude < 5).order_by(Star.star_id).all()

    star_data = []
    for star in stars:
        altAz = get_altaz(star)
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


def convert_line_to_pixel(const_line, direction):
    """Convert the start/end of a line (which are stars) to pixel coordinates"""

    start = const_line.startpoint
    end = const_line.endpoint

    start_star = Star.query.filter_by(star_id=start).one()
    end_star = Star.query.filter_by(star_id=end).one()

    start_position = get_altaz(start_star)
    end_position = get_altaz(end_star)

    start_xy = c.convert_sky_to_pixel(start_position.alt, start_position.az, direction)
    end_xy = c.convert_sky_to_pixel(end_position.alt, end_position.az, direction)

    return [start_xy, end_xy]


def create_list_of_constellations(star_list, direction):
    """create a list of dictionaries containing info about visible constellations"""

    star_ids = []
    for star in star_list:
        star_ids.append(star['id'])

    constellation_ids = []
    lines_in_frame = []
    constellations = []

    lines = Const_Line.query.all()

    for line in lines:
        if line.startpoint in star_ids:
            if line.endpoint in star_ids:
                lines_in_frame.append(line)

    for line in lines_in_frame:
        if line.const not in constellation_ids:
            constellation_ids.append(line.const)

    for const_id in constellation_ids:
        const = Constellation.query.filter_by(const_id=const_id).one()
        lines = []
        for line in lines_in_frame:
            if line.const == const_id:
                line = convert_line_to_pixel(line, direction)
                lines.append(line)

        constellation = {"id": const_id,
                         "name": const.name,
                         "lines": lines}
        constellations.append(constellation)

    return constellations
