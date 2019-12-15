import logging
from geoalchemy2 import WKTElement
from marshmallow import ValidationError

from app import db
from app.models import (
    Property,
    FederalUnity,
    Location,
    City,
    Neighbourhood,
    Street,
    PostalCode,
)
from app.gmaps import get_place_by_postal_code
from app.api.v1.serializers import PlaceReaderSchema

LOG = logging.getLogger(__name__)


def property_exists(postal_code, price, area):
    query = (
        db.session.query(Location)
        .join(Property)
        .filter(Location.postal_code == postal_code)
        .filter(Property.area == area)
        .filter(Property.price == price)
    )

    return query.filter(query.exists()).scalar()


def save_property(location, price, area, url):
    property = Property(location=location, price=price, area=area, url=url)
    db.session.add(property)
    db.session.commit()


def delete_property(id):
    property = Property.query.get_or_404(id)
    db.session.delete(property)
    db.session.commit()


def get_property(id):
    return Property.query.get_or_404(id)


def get_property_list(page, page_size):
    return Property.query.paginate(page, page_size, False)


def get_location_by_postal_code(postal_code):
    return Location.query.filter_by(postal_code=postal_code).one_or_none()


def create_location(postal_code):
    raw_place = get_place_by_postal_code(postal_code)
    if raw_place is None:
        raise Exception(f"Postal code {postal_code} returned no place.")
    try:
        place = PlaceReaderSchema().load(raw_place)
    except ValidationError as err:
        LOG.info(f"Google Places API returned an invalid value: {raw_place}")
        LOG.info(f"Validation error: {err}")
        raise Exception("Invalid place.")

    place = PlaceReaderSchema().load(raw_place)
    federal_unity = get_federal_unity(place["federal_unity"])
    city = get_city(place.get("city"), federal_unity)
    neighbourhood = get_neighbourhood(place.get("neighbourhood"), city)
    code = get_postal_code(postal_code, city)
    street = get_street(place.get("street"), code, neighbourhood)
    longitude = place["longitude"]
    latitude = place["latitude"]
    geom = WKTElement(f"POINT({longitude} {latitude})")
    return Location(
        street=street,
        latitude=longitude,
        longitude=latitude,
        places_id=place["places_id"],
        geom=geom,
        postal_code=postal_code,
    )


def get_federal_unity(federal_unity_data):
    short_name = federal_unity_data[0]
    return FederalUnity.query.filter_by(short_name=short_name).first_or_404(
        description=f"There is no '{short_name}' federal_unity"
    )
    return None


def get_city(name, federal_unity):
    city = City.query.filter_by(name=name).one_or_none()
    if city is not None:
        return city

    return City(name=name, federal_unity=federal_unity)


def get_neighbourhood(name, city):
    neighbourhood = Neighbourhood.query.filter_by(name=name).one_or_none()
    if neighbourhood is not None:
        return neighbourhood

    return Neighbourhood(name=name, city=city)


def get_postal_code(code, city):
    postal_code = PostalCode.query.filter_by(code=code).one_or_none()
    if postal_code is not None:
        return postal_code

    return PostalCode(code=code, city=city)


def get_street(name, postal_code, neighbourhood):
    street = Street.query.filter_by(name=name).one_or_none()
    if street is not None:
        return street

    return Street(name=name, neighbourhood=neighbourhood, postal_code=postal_code)
