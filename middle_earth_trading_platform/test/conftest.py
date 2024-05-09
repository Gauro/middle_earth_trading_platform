import pytest
from fastapi.testclient import TestClient

from middle_earth_trading_platform.main import app


@pytest.fixture(scope="module")
def client():
    with TestClient(app) as client:
        yield client
