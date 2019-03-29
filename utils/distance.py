"""
Implementation of the Haversine function for spherical distance calculations.
Adapted from Javascript code by Andrew Hedges:
    https://andrew.hedges.name/experiments/haversine/
"""

from typing import Tuple
from math import sin, cos, atan2, sqrt, radians

# Radius of Earth at Victoria, BC (48.4 degrees latitude) in metres
EARTH_RADIUS = 6366.223 * 1000


def haversine(x1: Tuple[float, float], x2: Tuple[float, float], earth_radius=EARTH_RADIUS):
    """Haversine algorithm for lat/long distances.
    :param x1 (Latitude, Longitude) for first point
    :param x2 (Latitude, Longitude) for second point
    :param earth_radius Radius of earth near the points
    :return Distance between x1 and x2 in metres."""
    x1_lat, x1_long = radians(x1[0]), radians(x1[1])
    x2_lat, x2_long = radians(x2[0]), radians(x2[1])

    d_long = x2_long - x1_long
    d_lat = x2_long - x1_long
    a = (sin(d_lat / 2)) ** 2 + cos(x1_lat) * cos(x2_lat) * (sin(d_long / 2)) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return earth_radius * c


if __name__ == "__main__":
    x1 = (48.41217789221235, -123.33804273564147)
    x2 = (48.41216174297099, -123.33803828530804)
    print(haversine(x1, x2))
