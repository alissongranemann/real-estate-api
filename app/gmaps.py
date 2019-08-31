import googlemaps
import os


def get_place_by_postal_code(postal_code):
    gmaps = googlemaps.Client(key=os.environ["GOOGLE_PLACES_API"])
    results = gmaps.geocode(address=postal_code, components={"country": "BR"})
    if results:
        geocode_result = results[0]
        return adapt_result(geocode_result)

    return None


def adapt_result(geocode_result):
    address_components = geocode_result.get("address_components", {})
    place = {}
    types = {
        "postal_code": "postal_code",
        "route": "street",
        "sublocality": "neighbourhood",
        "administrative_area_level_2": "city",
        "administrative_area_level_1": "state",
    }
    location = geocode_result.get("geometry", {}).get("location", {})
    place["latitude"] = location.get("lat")
    place["longitude"] = location.get("lng")
    place["places_id"] = geocode_result.get("place_id")
    for address_component in address_components:
        long_name = address_component.get("long_name")
        short_name = address_component.get("short_name")
        for key, value in types.items():
            if key in address_component.get("types"):
                place[value] = {"long_name": long_name, "short_name": short_name}
                del types[key]
                break

    return place
