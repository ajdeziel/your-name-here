"""
Gets long/lat coordinates from city names using Mapbox's geocoding api.
"""

import os
import requests

MAPBOX_API_KEY = os.environ.get("MAPBOX_API_KEY")


def geocode(country_name, city_name=None):
    query_string = country_name
    if city_name:
        query_string = "%s, %s" % (city_name, query_string)

    args = {
        "limit": 1,
        "types": "place",
        "access_token": MAPBOX_API_KEY
    }

    resp = requests.get("https://api.mapbox.com/geocoding/v5/mapbox.places/%s.json" % query_string, args)

    resp_json = resp.json()
    place_name = resp_json["features"][0]["place_name"]
    place_long = resp_json["features"][0]["geometry"]["coordinates"][0]
    place_lat = resp_json["features"][0]["geometry"]["coordinates"][1]

    return place_name, place_long, place_lat


if __name__ == "__main__":
    name, long, lat = geocode("Victoria", "Canada")
    print("%s: %f, %f" % (name, long, lat))
