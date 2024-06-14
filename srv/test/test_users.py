from test.client import client

def test_read_users():
    response = client.get("/api/read_users")
    assert response.status_code == 200