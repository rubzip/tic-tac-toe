import pytest

def test_create_game(client):
    response = client.post("/api/v1/game/new_game")
    assert response.status_code == 200
    data = response.json()
    assert "game_id" in data
    
def test_get_game(client):
    # Create a game first
    response = client.post("/api/v1/game/new_game")
    game_id = response.json()["game_id"]
    
    # Get the game
    response = client.get(f"/api/v1/game/{game_id}")
    assert response.status_code == 200
    data = response.json()
    assert "board" in data
    assert data["status"] == "KEEP_PLAYING"

def test_get_nonexistent_game(client):
    response = client.get("/api/v1/game/some_random_id")
    assert response.status_code == 404
