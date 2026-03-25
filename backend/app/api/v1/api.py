from fastapi import APIRouter
from app.api.v1.endpoints import game, websocket

api_router = APIRouter()

api_router.include_router(game.router, prefix="/game", tags=["game"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
