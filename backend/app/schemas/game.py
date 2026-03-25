from typing import List, Annotated
from pydantic import BaseModel, Field, RootModel
from ..core.constants import GameStatus, Player, UsablePlayer


class Move(BaseModel):
    row: Annotated[int, Field(ge=0, le=2)]
    col: Annotated[int, Field(ge=0, le=2)]


class Row(RootModel):
    root: List[Player] = Field(..., min_length=3, max_length=3)


class GameState(BaseModel):
    board: List[Row] = Field(..., min_length=3, max_length=3)
    turn: UsablePlayer
    status: GameStatus

    @classmethod
    def from_game(cls, game) -> "GameState":
        return cls(
            board=[Row(root=row) for row in game.get_board()],
            turn=game.get_turn(),
            status=game.get_game_status()
        )
