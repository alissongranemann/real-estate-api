def test_home(client):
    resp = client.get("/")
    message = str(resp.data, "utf-8")
    assert resp.status_code == 200
    assert "Up and running!" == message
