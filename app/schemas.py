from enum import StrEnum
from typing import List, Literal, Annotated
from pydantic import BaseModel, Field, RootModel


class GameStatus(StrEnum):
    WIN_X = "WIN_X"
    WIN_O = "WIN_O"
    DRAW = "DRAW"
    KEEP_PLAYING = "KEEP_PLAYING"


class Player(StrEnum):
    NONE = " "
    X = "X"
    O = "O"


UsablePlayer = Literal[Player.O, Player.X]


class Move(BaseModel):
    row: Annotated[int, Field(ge=0, le=2)]
    col: Annotated[int, Field(ge=0, le=2)]


class Row(RootModel):
    root: List[Player] = Field(..., min_length=3, max_length=3)


class GameState(BaseModel):
    board: List[List[Player]] = Field(..., min_length=3, max_length=3)
    turn: UsablePlayer
    status: GameStatus
