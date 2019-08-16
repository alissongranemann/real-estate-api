import json


def test_add_property(app):
    with app.test_client() as client:
        response = client.post(
            "/api/v1/properties",
            data=json.dumps(
                {
                    "area": 50,
                    "price": 50000.0,
                    "address": {"city": "City", "cep": "00000-000"},
                }
            ),
            content_type="application/json",
        )
        data = json.loads(response.data.decode())
        assert response.status_code == 201
        assert "" == data
