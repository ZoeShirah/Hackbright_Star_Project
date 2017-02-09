"""helper functions to calculate star locations"""
import sidereal.sidereal
from datetime import datetime


# coords = sidereal.sidereal.RADec(2.5297431200, 89.2641380500)

# h = coords.hourAngle(datetime.utcnow(), -122.4194155)

# sky_coords = coords.altAz(h, 37.7749295)

# print "sky coords of polaris", sky_coords


def get_current_altAz(ra, dec, lon=-122.4194155, lat=37.7749295):
    """Get current altaz coords for a star at given ra and dec, default observer in SF

    lat/long of SF = 37.7749295/-122.4194155
    """
    coords = sidereal.sidereal.RADec(ra, dec)
    h = coords.hourAngle(datetime.utcnow(), lon)
    sky_coords = coords.altAz(h, lat)
    return sky_coords

def visible_window(al, az):
    """Determine if a star is visible in one of the four windows"""
    pass


def convert_sky_to_northpixel(al, az):
    pass


def convert_sky_to_eastpixel(al, az):
    pass


def convert_sky_to_southhpixel(al, az):
    pass


def convert_sky_to_westpixel(al, az):
    pass

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
