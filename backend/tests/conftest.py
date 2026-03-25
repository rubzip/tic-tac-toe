import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.manager import manager

@pytest.fixture(autouse=True)
def cleanup_manager():
    """Clear games and connections before/after each test."""
    manager.active_connections.clear()
    manager.games.clear()
    yield

@pytest.fixture
def client():
    return TestClient(app)
