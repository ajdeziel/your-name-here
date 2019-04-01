import os
import requests

GOOGLEMAPS_API_KEY = os.environ.get("GOOGLEMAPS_API_KEY")


def geocode(place_name: str):
    args = {
        "address": place_name,
        "key": GOOGLEMAPS_API_KEY
    }

    resp = requests.get("https://maps.googleapis.com/maps/api/geocode/json", args)

    resp_json = resp.json()
    if len(resp_json["results"]) > 0:
        name_formatted = resp_json["results"][0]["formatted_address"]
        lat = resp_json["results"][0]["geometry"]["location"]["lat"]
        long = resp_json["results"][0]["geometry"]["location"]["lng"]

        return name_formatted, lat, long
    else:
        return None, None, None
