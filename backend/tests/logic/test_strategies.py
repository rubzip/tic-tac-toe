import pytest
from app.logic.strategies import (
    Board, 
    TicTacToeCPU, 
    GreedyStrategy, 
    StochasticStrategy, 
    RandomSmartStrategy
)
from app.core.constants import Player

def test_board_from_list():
    board_list = [
        [Player.X, Player.NONE, Player.NONE],
        [Player.NONE, Player.O, Player.NONE],
        [Player.NONE, Player.NONE, Player.NONE]
    ]
    board = Board.from_list(board_list)
    assert board.x_mask[0] is True
    assert board.o_mask[4] is True
    assert sum(board.x_mask) == 1
    assert sum(board.o_mask) == 1

def test_cpu_winning_move():
    cpu = TicTacToeCPU()
    board_list = [
        [Player.X, Player.X, Player.NONE],
        [Player.O, Player.O, Player.NONE],
        [Player.NONE, Player.NONE, Player.NONE]
    ]
    board = Board.from_list(board_list)
    moves = cpu.get_possible_moves(board, is_x=True)
    assert moves[2][0] == 1.0  # Winning move for X

def test_greedy_strategy():
    strategy = GreedyStrategy()
    board = [
        [Player.X, Player.X, Player.NONE],
        [Player.O, Player.O, Player.NONE],
        [Player.NONE, Player.NONE, Player.NONE]
    ]
    move = strategy.get_move(board, is_x=True)
    assert move == (0, 2)

def test_random_smart_strategy():
    strategy = RandomSmartStrategy()
    board = [
        [Player.X, Player.X, Player.NONE],
        [Player.O, Player.O, Player.NONE],
        [Player.NONE, Player.NONE, Player.NONE]
    ]
    move = strategy.get_move(board, is_x=True)
    assert move == (0, 2)
