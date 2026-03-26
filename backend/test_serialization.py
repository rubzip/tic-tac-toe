import sys
import os
sys.path.append(os.getcwd())

from app.logic.tic_tac_toe import Game
from app.schemas.game import GameState
from app.core.constants import Player

def test_serialization():
    game = Game()
    try:
        state = GameState.from_game(game)
        print("Serialization successful!")
        print("JSON output:", state.model_dump_json())
    except Exception as e:
        print("Serialization failed!")
        print(f"Error: {e}")

if __name__ == "__main__":
    test_serialization()
