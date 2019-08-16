def test_home(app):
    client = app.test_client()
    resp = client.get("/")
    message = str(resp.data, "utf-8")
    assert resp.status_code == 200
    assert "Up and running!" == message
