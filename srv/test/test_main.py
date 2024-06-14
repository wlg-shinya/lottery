import sys
sys.path = ['', '..'] + sys.path[1:]

from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_foo():
    assert True == False