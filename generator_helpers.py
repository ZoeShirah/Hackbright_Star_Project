import calculations as c
from datetime import datetime
from flask import session
from model import Star, Const_Line, Constellation
from sqlalchemy import or_
import ephem


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

            const_list = get_list_of_constellations(star.star_id)
            if len(const_list) > 0:
                star_info.update({'constellations': const_list})

            star_data.append(star_info)

    return star_data


def get_list_of_constellations(star_id):
    """Get a list of constellations a particular star is in"""
    lines = Const_Line.query.filter(or_(Const_Line.startpoint == star_id, Const_Line.endpoint == star_id)).all()
    if lines:
        consts = set()
        for line in lines:
            name = line.constellation.name
            name = c.replace_constellation_name(name)
            consts.add(name)
        return list(set(consts))
    else:
        return []


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
    """create a dictionary containing info about visible constellations"""

    star_ids = []
    for star in star_list:
        star_ids.append(star['id'])

    constellation_ids = []
    lines_in_frame = []
    constellations = []

    lines = Const_Line.query.all()

    # gets lines where the full line is actually in the frame
    for line in lines:
        if line.startpoint in star_ids:
            if line.endpoint in star_ids:
                lines_in_frame.append(line)

    # gets a list of all the constellations those lines belong to
    for line in lines_in_frame:
        if line.const not in constellation_ids:
            constellation_ids.append(line.const)

    # creates dictionary for each constellation with name and id
    for const_id in constellation_ids:
        const = Constellation.query.filter_by(const_id=const_id).one()
        name = c.replace_constellation_name(const.name)
        constellation = {"id": const_id,
                         "name": name}
        constellations.append(constellation)

    #creates list of lines with pixel coordinate start and end points
    lines = []
    for line in lines_in_frame:
        line = convert_line_to_pixel(line, direction)
        lines.append(line)

    constellation_info = {"constellations": constellations,
                          "lines": lines}

    return constellation_info


def get_planet_info(date, lat, lon, direction):
    """Get info about planets visible at a time and location, return a list of dictionaries"""

    observer = ephem.Observer()
    observer.lat = lat
    observer.lon = lon
    observer.date = date
    print "date", observer.date, "lat", observer.lat, lat

    sun = {"name": "Sun", "info": ephem.Sun(), "color": "#ffffcc"}
    mercury = {"name": "Mercury", "info": ephem.Mercury(), "color": "##ffe5bf"}
    venus = {"name": "Venus", "info": ephem.Venus(), "color": "white"}
    moon = {"name": "Moon", "info": ephem.Moon(), "color": "#fffcf9"}
    mars = {"name": "Mars", "info": ephem.Mars(), "color": "#ffd1ba"}
    jupiter = {"name": "Jupiter", "info": ephem.Jupiter(), "color": "#fff6e0"}
    saturn = {"name": "Saturn", "info": ephem.Saturn(), "color": "#fcd9b0"}
    uranus = {"name": "Uranus", "info": ephem.Uranus(), "color": "#d4fcd6"}
    neptune = {"name": "Neptune", "info": ephem.Neptune(), "color": "#bad4ff"}

    planets = [sun, mercury, venus, moon, mars, jupiter, saturn, uranus, neptune]

    planet_info = []
    for planet in planets:
        planet['info'].compute(observer)
        print planet['info'].alt, planet['info'].az, repr(planet['info'].alt)
        planet['alt'] = planet['info'].alt
        planet['az'] = planet['info'].az
        print planet['alt'], planet['az'], planet['name']
        visible = c.get_visible_window(planet['alt'], planet['az'])
        print visible
        if direction in visible:
            if planet['info'].mag > 5:
                continue
            coords = c.convert_sky_to_pixel(planet['alt'], planet['az'], direction)
            planet.update(coords)
            planet['magnitude'] = planet['info'].mag
            planet['constellation'] = ephem.constellation(planet['info'])[1]
            planet.pop('info', None)
            planet_info.append(planet)

    return planet_info
