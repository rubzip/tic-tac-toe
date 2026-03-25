import pytest
from app.schemas.game import Move, GameState, Row
from app.core.constants import Player, GameStatus

def test_move_validation():
    # Valid move
    move = Move(row=0, col=2)
    assert move.row == 0
    assert move.col == 2
    
    # Invalid move (out of bounds)
    with pytest.raises(ValueError):
        Move(row=3, col=0)

def test_game_state_schema():
    board = [
        Row(root=[Player.X, Player.NONE, Player.NONE]),
        Row(root=[Player.NONE, Player.O, Player.NONE]),
        Row(root=[Player.NONE, Player.NONE, Player.NONE])
    ]
    state = GameState(board=board, turn=Player.X, status=GameStatus.KEEP_PLAYING)
    assert state.turn == Player.X
    assert len(state.board) == 3
