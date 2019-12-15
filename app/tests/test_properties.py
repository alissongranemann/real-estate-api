import json
import pytest

from app.models import (
    Property,
    Location,
    FederalUnity,
    City,
    Street,
    Neighbourhood,
    PostalCode,
)
from geoalchemy2 import WKTElement
from unittest.mock import patch


def persist(db, model):
    db.session.add(model)
    db.session.commit()


@pytest.fixture()
def federal_unity(db):
    federal_unity = FederalUnity(name="Santa Catarina", short_name="SC")
    persist(db, federal_unity)
    return federal_unity


@pytest.fixture()
def city(db, federal_unity):
    city = City(name="Florianópolis", federal_unity=federal_unity)
    persist(db, city)
    return city


@pytest.fixture()
def neighbourhood(db, city):
    neighbourhood = Neighbourhood(name="Trindade", city=city)
    persist(db, neighbourhood)
    return neighbourhood


@pytest.fixture()
def postal_code(db, city):
    postal_code = PostalCode(city=city, code="88040-000")
    persist(db, postal_code)
    return postal_code


@pytest.fixture()
def street(db, neighbourhood, postal_code):
    street = Street(
        name="Lauro Linhares", neighbourhood=neighbourhood, postal_code=postal_code
    )
    persist(db, street)
    return street


@pytest.fixture()
def location(db, street, postal_code):
    longitude = 10.20
    latitude = -20.10
    geom = WKTElement(f"POINT({longitude} {latitude})")
    location = Location(
        street=street,
        latitude=latitude,
        longitude=longitude,
        places_id="12345ab",
        geom=geom,
        postal_code=postal_code.code,
    )
    persist(db, location)
    return location


@pytest.fixture()
def property(db, federal_unity, city, neighbourhood, street, location):
    property = Property(
        price=50000.0, area=40, location=location, url="http://site.com"
    )
    db.session.add(property)
    db.session.commit()
    return property


@pytest.fixture()
def properties(db, federal_unity, property, city, neighbourhood, street, location):
    property2 = Property(
        price=75000.0, area=55, location=location, url="http://site.com"
    )
    db.session.add(property2)
    property3 = Property(
        price=110000.0, area=80, location=location, url="http://site.com"
    )
    db.session.add(property3)
    db.session.commit()

    return [property, property2, property3]


@pytest.fixture
def scrapped_property():
    return {
        "area": 50,
        "price": 50000.0,
        "postal_code": "88040-000",
        "url": "http://site.com",
    }


@pytest.fixture
def place():
    return {
        "postal_code": {"long_name": "88040-000", "short_name": "88040-000"},
        "street": {
            "long_name": "Rua Deputado Antônio Edu Vieira",
            "short_name": "R. Dep. Antônio Edu Vieira",
        },
        "neighbourhood": {"long_name": "Pantanal", "short_name": "Pantanal"},
        "city": {"long_name": "Florianópolis", "short_name": "Florianópolis"},
        "federal_unity": {"long_name": "Santa Catarina", "short_name": "SC"},
        "latitude": -27.6090093,
        "longitude": -48.5215363,
        "places_id": "ChIJn4fZaqg5J5URBkczejLhp_4",
    }


@patch("app.services.get_place_by_postal_code")
def test_add_property(
    mock_get_place_by_postal_code, client, federal_unity, scrapped_property, place
):
    mock_get_place_by_postal_code.return_value = place
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(scrapped_property),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert "" == data


@patch("app.services.get_place_by_postal_code")
def test_add_existent_property(
    mock_get_place_by_postal_code, client, federal_unity, scrapped_property, place
):
    mock_get_place_by_postal_code.return_value = place
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(scrapped_property),
        content_type="application/json",
    )
    assert response.status_code == 201
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(scrapped_property),
        content_type="application/json",
    )
    assert response.status_code == 303


def test_add_invalid_price_property(client, scrapped_property):
    invalid_property = scrapped_property
    invalid_property["price"] = "invalid"
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(invalid_property),
        content_type="application/json",
    )
    assert response.status_code == 400
    print(response)
    data = json.loads(response.data.decode())
    errors = data.get("errors")
    assert errors is not None
    price_error = errors.get("price")
    assert price_error is not None
    assert len(price_error) == 1
    assert "not a valid number" in price_error[0].lower()


def test_add_invalid_area_property(client, scrapped_property):
    invalid_property = scrapped_property
    invalid_property["area"] = "invalid"
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(invalid_property),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    errors = data.get("errors")
    assert errors is not None
    area_error = errors.get("area")
    assert area_error is not None
    assert len(area_error) == 1
    assert "not a valid integer" in area_error[0].lower()


def test_add_invalid_cep_property(client, scrapped_property):
    invalid_property = scrapped_property
    invalid_property["postal_code"] = "invalid"
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(invalid_property),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    errors = data.get("errors")
    assert errors is not None
    postal_code_error = errors.get("postal_code")
    assert postal_code_error is not None
    assert len(postal_code_error) == 1
    assert "must follow the #####-### pattern" in postal_code_error[0]


def test_delete_property(client, property):
    response = client.delete(f"/api/v1/properties/{property.id}")
    assert response.status_code == 204
    assert Property.query.count() == 0


def test_get_property(client, property):
    response = client.get(f"/api/v1/properties/{property.id}")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert len(data) == 4
    area = data.get("area")
    assert area == 40
    price = data.get("price")
    assert price == 50000.0
    location = data.get("location")
    assert len(location) == 5
    street = location.get("street")
    assert street.get("name") == "Lauro Linhares"
    postal_code = street.get("postal_code")
    assert postal_code.get("code") == "88040-000"
    neighbourhood = street.get("neighbourhood")
    assert neighbourhood.get("name") == "Trindade"
    city = neighbourhood.get("city")
    assert city.get("name") == "Florianópolis"
    federal_unity = city.get("federal_unity")
    assert len(federal_unity) == 3
    short_name = federal_unity.get("short_name")
    assert short_name == "SC"
    name = federal_unity.get("name")
    assert name == "Santa Catarina"
    places_id = location.get("places_id")
    assert places_id == "12345ab"
    latitude = location.get("latitude")
    assert latitude == -20.10
    longitude = location.get("longitude")
    assert longitude == 10.20


def test_get_properties(client, properties):
    response = client.get(f"/api/v1/properties")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    page = data.get("data")
    assert len(page) == 3
    total = data.get("total")
    assert total == 3
