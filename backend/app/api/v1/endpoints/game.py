from fastapi import APIRouter, HTTPException
from app.services.manager import manager
from app.schemas.game import GameState

router = APIRouter()


@router.post("/new_game")
async def new_game():
    game_id = manager.add_new_game()
    return {"game_id": game_id}


@router.get("/{game_id}", response_model=GameState)
async def get_game(game_id: str):
    if game_id not in manager.games:
        raise HTTPException(status_code=404, detail="Game not found")
    return GameState.from_game(manager.games[game_id])
