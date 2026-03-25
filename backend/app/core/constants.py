from enum import StrEnum
from typing import Literal


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
