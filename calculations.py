"""helper functions to calculate star locations"""
import sidereal.sidereal
from datetime import datetime
import math

def get_current_altAz(ra, dec, lon=-122.4194155, lat=37.7749295):
    """Get current altaz coords for a star at given ra and dec, default observer in SF

    lat/long of SF = 37.7749295/-122.4194155
    """
    coords = sidereal.sidereal.RADec(ra, dec)
    h = coords.hourAngle(datetime.utcnow(), lon)
    sky_coords = coords.altAz(h, lat)
    return sky_coords


def visible_window(alt, az):
    """Determine if a star is visible in one of the four windows, return the window

    >>> visible_window(math.pi/4, math.pi/3)
    {'direction': ['North', 'East']}

    >>> visible_window(math.pi/4, math.pi/2)
    {'direction': ['East']}

    >>> visible_window(-math.pi/4, math.pi/3)
    {'direction': 'not visible'}

    """

    window = []
    if 0 <= alt <= math.pi/2:
        if 3*math.pi/2 < az or az < math.pi/2:
            window.append("North")
        if 0 < az < math.pi:
            window.append("East")
        if math.pi/2 < az < 3*math.pi/2:
            window.append("South")
        if math.pi < az < 2*math.pi:
            window.append("West")
    else:
        return {"direction": "not visible"}
    return {"direction": window}


def convert_sky_to_pixel(al, az):
    """Take altitude and azimuth and convert to pixel coords.

        pixel canvas size = 630px height(altitude) x 1260px width(azimuth)

        Total azimuth range = pi, to convert from a given az to a px:
        givenAz * maxPx/maxAz = givenAz * (1260/pi) = px

        Total altitude range is pi/2, so
        givenAl * maxPx/maxAl
                    = givenAl *(630/(math.pi/2)) = givenAL *(1260/math.pi) = py

    """
    px = (1260/math.pi) * az
    py = (1260/math.pi) * al
    return (px, py)


#north = 0 degrees azimuth, view for north facing window is going to be
#270 degrees to 90 degrees going clockwise (-90 to 90)  altitude is degrees
#above the horizon (0 to 90)

#north window will be azimuth 305 degrees to 55 degrees, altitude about 0 to 80
#so it will see 90 degrees up and 110 degrees side to side
#south window will be
#east window will be
#west window will be

#size of pixel image = 630h (altitude) 770w (azimuth)
#SF long/lat = -122.4194155/37.7749295

#sky coords of polaris [az 348d 16' 25.097" alt -6d 07' 30.753"]
