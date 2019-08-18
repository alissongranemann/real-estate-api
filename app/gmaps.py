import googlemaps
import os

ISO_CODE = "BR"


def get_place_by_zip_code(zip_code):
    gmaps = googlemaps.Client(key=os.environ["GOOGLE_PLACES_API"])
    results = gmaps.geocode(f"{zip_code}, {ISO_CODE}")
    print(results)
    if results:
        geocode_result = results[0]
        geometry = geocode_result.get("geometry")
        id = geocode_result.get("place_id")
        return dict(id=id, geometry=geometry)

    return None
