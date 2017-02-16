"""helper functions to calculate star locations"""

from sidereal import sidereal
from datetime import datetime
import math
from decimal import Decimal


def convert_degrees_to_radians(decimaldegree):
    return Decimal(decimaldegree)*Decimal(math.pi/180)


def get_current_altAz(ra, dec, lon=-2.1366218688, lat=0.65929689448, time=datetime.utcnow()):
    """Get current altaz coords for a star at given ra, dec, lat, long, datetime

    default observer in SF at now.
    Rad/dec and lat/long must be in radians, time must be UTC time as a datetime object

    lat/long of SF = 37.7749295/-122.4194155 degrees
                   = 0.65929689448/-2.1366218688 radians
    """
    coords = sidereal.RADec(ra, dec)
    h = coords.hourAngle(time, lon)
    sky_coords = coords.altAz(h, lat)
    return sky_coords


def get_visible_window(alt, az):
    """Determine if a star is visible in one of the four windows, return the window

    a star is visible in a window if it is in within pi/3 radians of the center
    point of the direction, where north = 0, east = pi/2, south = pi, west = 3pi/2

    >>>  get_visible_window(math.pi/2, math.pi/3)
    ['North', 'East']

    >>> get_visible_window(math.pi/4, math.pi/2)
    ['East']

    >>> get_visible_window(-math.pi/4, math.pi/3)
    []

    """

    window = []
    if 0 <= alt <= math.pi/2:
        if 5*math.pi/3 <= az or az <= math.pi/3:
            window.append("North")
        if math.pi/6 <= az <= 5*math.pi/6:
            window.append("East")
        if 2*math.pi/3 <= az <= 4*math.pi/3:
            window.append("South")
        if 7*math.pi/6 <= az <= 11*math.pi/6:
            window.append("West")
    return window


def convert_sky_to_pixel(alt, az, direction):
    """Take altitude and azimuth and convert to pixel coords.

        pixel canvas size = 600px height(altitude) x 800px width(azimuth)

        Total azimuth range = 2pi/3, to convert from a given az to a px:
        givenAz * maxPx/maxAz = givenAz * (800/(2pi/3)
                                = givenAz *(1200/math.pi)

        Total altitude range is pi/2, so
        givenAl * maxPx/maxAlt
                   = givenAlt *(600/(math.pi/2)) = givenALt *(1200/math.pi) = py

    """
    if direction == "East":
        az = az - (math.pi/6)
    if direction == "South":
        az = az - (2*math.pi/3)
    if direction == "West":
        az = az - (7*math.pi/6)
    if direction == "North":
        if az >= 5*math.pi/3:
            az = az - (5*math.pi/3)
        elif az <= math.pi/3:
            az = az + math.pi/3

    px = az*(1200.0/math.pi)
    py = 600.0 - ((1200.0/math.pi) * alt)

    return {"x": px,
            "y": py}


def get_color(colorIndex):
    if colorIndex <= 0.15:  # blue is about -0.33 to 0.15
        color = "#e8f0ff"
    elif colorIndex < 0.6:  # white from 0.15 to 0.6
        color = "white"
    elif colorIndex < 1.15:  # yellow 0.6 to 1.15
        color = "#fffbd1"
    elif colorIndex < 1.64:  # orange 1.15 to 1.64
        color = "#ffd9b3"
    elif colorIndex >= 1.64:  # red = greater than 1.64
        color = "#ffc6c6"

    return color


#north = 0 degrees azimuth, view for north facing window is going to be
#270 degrees to 90 degrees going clockwise (-90 to 90)  altitude is degrees
#above the horizon (0 to 90)

#north window will be azimuth 305 degrees to 55 degrees, altitude about 0 to 80
#so it will see 90 degrees up and 110 degrees side to side
#south window will be
#east window will be
#west window will be

#size of pixel image = 630px height(altitude) x 1260px width(azimuth)
#SF long/lat = -122.4194155/37.7749295
