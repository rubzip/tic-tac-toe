import uuid
from fastapi import WebSocket
from .models import TicTacToe
from .schemas import GameState


class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
        self.games: dict[str, TicTacToe] = {}
    
    def add_new_game(self) -> str:
        game_id = str(uuid.uuid4())
        while game_id in self.games:
            game_id = str(uuid.uuid4())
        self.games[game_id] = TicTacToe()
        self.active_connections[game_id] = []
        return game_id

    async def connect(self, websocket: WebSocket, game_id: str):
        await websocket.accept()
        if game_id not in self.active_connections:
            self.active_connections[game_id] = []
            self.games[game_id] = TicTacToe()
        self.active_connections[game_id].append(websocket)

    def disconnect(self, websocket: WebSocket, game_id: str):
        if game_id in self.active_connections:
            self.active_connections[game_id].remove(websocket)
            if not self.active_connections[game_id]:
                # Optionally cleanup game if no one is connected
                # del self.active_connections[game_id]
                # del self.games[game_id]
                pass

    async def broadcast(self, game_id: str) -> None:
        """Sends the current state to ALL players of that game."""
        if game_id not in self.games:
            return

        state = self.games[game_id].get_state()
        message = state.model_dump()

        for connection in self.active_connections.get(game_id, []):
            await connection.send_json(message)
