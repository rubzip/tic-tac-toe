from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from pydantic import ValidationError

from .models import TicTacToe
from .schemas import GameStatus, UsablePlayer, Move, GameState, Player
from .manager import ConnectionManager


app = FastAPI(title="Tic-Tac-Toe LAN")
manager = ConnectionManager()


@app.websocket("/ws/{game_id}/{player}")
async def websocket_endpoint(websocket: WebSocket, game_id: str, player: UsablePlayer):
    if (
        game_id not in manager.games and player != Player.X
    ):  # Optional: only first player can create
        # Actually, current logic creates game on connect.
        pass

    await manager.connect(websocket, game_id)
    await manager.broadcast(game_id)

    try:
        while True:
            data = await websocket.receive_json()

            try:
                move = Move(**data)
                game = manager.games[game_id]

                if game.get_game_status() != GameStatus.KEEP_PLAYING:
                    await websocket.send_json({"error": "El juego ya terminó"})
                    continue

                game.put(move, player)
                await manager.broadcast(game_id)
            except (ValueError, ValidationError) as e:
                await websocket.send_json({"error": str(e)})
            except Exception:
                await websocket.send_json({"error": "Formato de mensaje inválido"})

    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)


@app.websocket("/ws/{game_id}/")
async def spectator_endpoint(websocket: WebSocket, game_id: str):
    await manager.connect(websocket, game_id)
    await manager.broadcast(game_id)

    try:
        while True:
            await websocket.receive_text()  # Just keep alive or wait for ignore
    except WebSocketDisconnect:
        manager.disconnect(websocket, game_id)


@app.post("/new_game")
async def new_game():
    game_id = manager.add_new_game()
    return {"game_id": game_id}


@app.get("/game/{game_id}", response_model=GameState)
async def get_game(game_id: str):
    if game_id not in manager.games:
        raise HTTPException(status_code=404, detail="Game not found")
    return manager.games[game_id].get_state()
