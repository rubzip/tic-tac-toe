from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from pydantic import ValidationError
from app.services.manager import manager
from app.core.constants import Player, GameStatus, UsablePlayer
from app.schemas.game import Move

router = APIRouter()


@router.websocket("/{game_id}/{player}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player: UsablePlayer):
    await manager.connect(websocket, game_id)
    await manager.broadcast(game_id)

    try:
        while True:
            data = await websocket.receive_json()

            try:
                move = Move(**data)
                if game_id not in manager.games:
                    await websocket.send_json({"error": "Juego no encontrado"})
                    continue

                game = manager.games[game_id]

                if game.get_game_status() != GameStatus.KEEP_PLAYING:
                    await websocket.send_json({"error": "El juego ya terminó"})
                    continue

                try:
                    game.put(move, player)
                    await manager.broadcast(game_id)
                except ValueError as e:
                    await websocket.send_json({"error": str(e)})

            except (ValidationError, Exception) as e:
                await websocket.send_json({"error": "Formato de mensaje inválido"})

    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)


@router.websocket("/{game_id}/")
async def spectator_endpoint(websocket: WebSocket, game_id: str):
    await manager.connect(websocket, game_id)
    await manager.broadcast(game_id)

    try:
        while True:
            await websocket.receive_text()  # Keep alive
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)
