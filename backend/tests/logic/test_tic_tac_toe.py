import pytest
from app.logic.tic_tac_toe import Game, TicTacToeEngine
from app.core.constants import Player, GameStatus

def test_engine_victory():
    board = [
        [Player.X, Player.X, Player.X],
        [Player.O, Player.NONE, Player.O],
        [Player.NONE, Player.NONE, Player.NONE]
    ]
    assert TicTacToeEngine.get_game_status(board) == GameStatus.WIN_X

def test_engine_draw():
    board = [
        [Player.X, Player.O, Player.X],
        [Player.X, Player.O, Player.O],
        [Player.O, Player.X, Player.X]
    ]
    assert TicTacToeEngine.get_game_status(board) == GameStatus.DRAW

def test_game_full_flow():
    game = Game(start_player=Player.X)
    game.put(0, 0, Player.X)
    assert game.turn == Player.O
    game.put(1, 1, Player.O)
    assert game.turn == Player.X
    game.put(0, 1, Player.X)
    game.put(2, 2, Player.O)
    game.put(0, 2, Player.X)
    assert game.get_game_status() == GameStatus.WIN_X
    assert game.turn == Player.NONE

def test_game_invalid_move():
    game = Game()
    game.put(0, 0, Player.O)
    with pytest.raises(ValueError, match="Occupied cell"):
        game.put(0, 0, Player.X)
    
    with pytest.raises(ValueError, match="Now is X turn"):
        game.put(1, 1, Player.O)
