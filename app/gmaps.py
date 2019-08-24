import googlemaps
import os

ISO_CODE = "BR"


def get_place_by_postal_code(postal_code):
    gmaps = googlemaps.Client(key=os.environ["GOOGLE_PLACES_API"])
    results = gmaps.geocode(f"{postal_code}, {ISO_CODE}")
    if results:
        geocode_result = results[0]
        return serialize(geocode_result)

    return None


def serialize(geocode_result):
    address_components = geocode_result["address_components"]
    place = {}
    types = {
        "postal_code": "postal_code",
        "route": "street",
        "sublocality": "neighbourhood",
        "administrative_area_level_2": "city",
        "administrative_area_level_1": "state",
    }
    for address_component in address_components:
        long_name = address_component["long_name"]
        short_name = address_component["short_name"]
        for key, value in types.items():
            if key in address_component["types"]:
                place[value] = {"long_name": long_name, "short_name": short_name}
                del types[key]
                break

    location = geocode_result["geometry"]["location"]
    place["latitude"] = location["lat"]
    place["longitude"] = location["lng"]
    place["places_id"] = geocode_result["place_id"]

    return place
