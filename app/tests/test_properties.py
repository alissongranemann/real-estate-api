import json

from app.models import Property, Location, State
from geoalchemy2 import WKTElement
from unittest.mock import patch


def get_valid_property(area=50, price=50000.0, postal_code="88040-000"):
    return {
        "area": area,
        "price": price,
        "postal_code": postal_code,
        "url": "http://site.com",
        # "origin": "origin",
    }


def get_valid_place():
    return {
        "postal_code": {"long_name": "88040-000", "short_name": "88040-000"},
        "street": {
            "long_name": "Rua Deputado Antônio Edu Vieira",
            "short_name": "R. Dep. Antônio Edu Vieira",
        },
        "neighbourhood": {"long_name": "Pantanal", "short_name": "Pantanal"},
        "city": {"long_name": "Florianópolis", "short_name": "Florianópolis"},
        "state": {"long_name": "Santa Catarina", "short_name": "SC"},
        "latitude": -27.6090093,
        "longitude": -48.5215363,
        "places_id": "ChIJn4fZaqg5J5URBkczejLhp_4",
    }


@patch("app.api.views.get_place_by_postal_code")
def test_add_property(mock_get_place_by_postal_code, client):
    mock_get_place_by_postal_code.return_value = get_valid_place()
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(get_valid_property(100, 100000.0)),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert "" == data


@patch("app.api.views.get_place_by_postal_code")
def test_add_existent_property(mock_get_place_by_postal_code, client):
    mock_get_place_by_postal_code.return_value = get_valid_place()
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(get_valid_property(100, 100000.0)),
        content_type="application/json",
    )
    assert response.status_code == 201
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(get_valid_property(100, 100000.0)),
        content_type="application/json",
    )
    assert response.status_code == 303


def test_add_invalid_price_property(client):
    invalid_property = get_valid_property()
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


def test_add_invalid_area_property(client):
    invalid_property = get_valid_property()
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


def test_add_invalid_cep_property(client):
    invalid_property = get_valid_property()
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


def test_delete_property(client, db):
    property = save_new_property(db)

    response = client.delete(f"/api/v1/properties/{property.id}")
    assert response.status_code == 204
    assert Property.query.count() == 0


def test_get_property(client, db):
    property = save_new_property(db)

    response = client.get(f"/api/v1/properties/{property.id}")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    assert len(data) == 4
    area = data.get("area")
    assert area == 40
    price = data.get("price")
    assert price == 50000.0
    location = data.get("location")
    assert len(location) == 9
    city = location.get("city")
    assert city == "Florianópolis"
    postal_code = location.get("postal_code")
    assert postal_code == "00000-000"
    neighbourhood = location.get("neighbourhood")
    assert neighbourhood == "Bairro teste"
    street = location.get("street")
    assert street == "Rua teste"
    places_id = location.get("places_id")
    assert places_id == "12345ab"
    latitude = location.get("latitude")
    assert latitude == -20.10
    longitude = location.get("longitude")
    assert longitude == 10.20
    state = location.get("state")
    assert len(state) == 3
    initials = state.get("initials")
    assert initials == "SC"
    description = state.get("description")
    assert description == "Santa Catarina"


def test_get_properties(client, db):
    save_new_property(db, "00000-000", "12345ab")
    save_new_property(db, "00000-001", "12345cd")
    save_new_property(db, "00000-002", "12345ef")

    response = client.get(f"/api/v1/properties")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    page = data.get("data")
    assert len(page) == 3
    total = data.get("total")
    assert total == 3


def save_new_property(db, postal_code="00000-000", places_id="12345ab"):
    state = State(initials="SC", description="Santa Catarina")
    longitude = 10.20
    latitude = -20.10
    geom = WKTElement(f"POINT({longitude} {latitude})")
    location = Location(
        state=state,
        postal_code=postal_code,
        street="Rua teste",
        neighbourhood="Bairro teste",
        city="Florianópolis",
        latitude=latitude,
        longitude=longitude,
        places_id=places_id,
        geom=geom,
    )
    property = Property(
        price=50000.0, area=40, location=location, url="http://site.com"
    )
    db.session.add(property)
    db.session.commit()
    return property
