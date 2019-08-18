import json

from app.models import Property, Address


def get_valid_property():
    return {
        "area": 50,
        "price": 50000.0,
        "address": {"city": "City", "cep": "00000-000"},
    }


def test_add_property(client):
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(get_valid_property()),
        content_type="application/json",
    )
    data = json.loads(response.data.decode())
    assert response.status_code == 201
    assert "" == data


def test_add_invalid_price_property(client):
    invalid_property = get_valid_property()
    invalid_property["price"] = "price"
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(invalid_property),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    errors = data.get("errors")
    assert errors is not None
    price_error = errors.get("price")
    assert price_error is not None
    assert len(price_error) == 1
    assert "not a valid number" in price_error[0].lower()


def test_add_invalid_area_property(client):
    invalid_property = get_valid_property()
    invalid_property["area"] = "area"
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
    invalid_property["address"]["cep"] = "invalid"
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(invalid_property),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    errors = data.get("errors")
    assert errors is not None
    address_error = errors.get("address")
    assert address_error is not None
    cep_error = address_error.get("cep")
    assert cep_error is not None
    assert len(cep_error) == 1
    assert "must follow the #####-### pattern" in cep_error[0]


def test_add_invalid_city_property(client):
    invalid_property = get_valid_property()
    invalid_property["address"].pop("city")
    response = client.post(
        "/api/v1/properties",
        data=json.dumps(invalid_property),
        content_type="application/json",
    )
    assert response.status_code == 400
    data = json.loads(response.data.decode())
    errors = data.get("errors")
    assert errors is not None
    address_error = errors.get("address")
    assert address_error is not None
    city_error = address_error.get("city")
    assert city_error is not None
    assert len(city_error) == 1
    assert "required field" in city_error[0]


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
    address = data.get("address")
    assert len(address) == 4
    city = address.get("city")
    assert city == "Florianopolis"
    cep = address.get("cep")
    assert cep == "00000-000"
    neighbourhood = address.get("neighbourhood")
    assert neighbourhood is None


def test_get_properties(client, db):
    save_new_property(db)
    save_new_property(db)
    save_new_property(db)

    response = client.get(f"/api/v1/properties")
    assert response.status_code == 200
    data = json.loads(response.data.decode())
    page = data.get("data")
    assert len(page) == 3
    total = data.get("total")
    assert total == 3


def save_new_property(db):
    address = Address(city="Florianopolis", cep="00000-000")
    property = Property(price=50000.0, area=40, address=address)
    db.session.add(property)
    db.session.commit()
    return property
