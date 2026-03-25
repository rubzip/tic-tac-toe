from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Iterable, Optional
import math
import random
from app.core.constants import Player


WINNING_COMBOS = [
    (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
    (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
    (0, 4, 8), (2, 4, 6)              # Diagonals
]

SYMMETRIES = [
    (0, 1, 2, 3, 4, 5, 6, 7, 8),  # Identity
    (6, 3, 0, 7, 4, 1, 8, 5, 2),  # Rotation 90°
    (8, 7, 6, 5, 4, 3, 2, 1, 0),  # Rotation 180°
    (2, 5, 8, 1, 4, 7, 0, 3, 6),  # Rotation 270°
    (2, 1, 0, 5, 4, 3, 8, 7, 6),  # Horizontal Reflection
    (6, 7, 8, 3, 4, 5, 0, 1, 2),  # Vertical Reflection
    (0, 3, 6, 1, 4, 7, 2, 5, 8),  # Main Diagonal
    (8, 5, 2, 7, 4, 1, 6, 3, 0),  # Secondary Diagonal
]

@dataclass(frozen=True)
class Result:
    x_win: int = 0
    o_win: int = 0
    draw: int = 0

    def __add__(self, other: "Result") -> "Result":
        return Result(
            x_win=self.x_win + other.x_win,
            o_win=self.o_win + other.o_win,
            draw=self.draw + other.draw
        )

@dataclass(frozen=True, order=True)
class Board:
    x_mask: Tuple[bool, ...] = (False,) * 9
    o_mask: Tuple[bool, ...] = (False,) * 9

    @classmethod
    def from_list(cls, board: list[list[Player]]) -> 'Board':
        x_mask = [False] * 9
        o_mask = [False] * 9
        for i in range(3):
            for j in range(3):
                if board[i][j] == Player.X:
                    x_mask[i * 3 + j] = True
                elif board[i][j] == Player.O:
                    o_mask[i * 3 + j] = True
        return cls(tuple(x_mask), tuple(o_mask))

    def get_canonical_state(self) -> Tuple[Tuple[bool, ...], Tuple[bool, ...]]:
        variants = []
        for sym in SYMMETRIES:
            v_x = tuple(self.x_mask[i] for i in sym)
            v_o = tuple(self.o_mask[i] for i in sym)
            variants.append((v_x, v_o))
        return min(variants)

    def is_win(self, is_x: bool) -> bool:
        mask = self.x_mask if is_x else self.o_mask
        return any(all(mask[pos] for pos in combo) for combo in WINNING_COMBOS)

    def is_full(self) -> bool:
        return all(x or o for x, o in zip(self.x_mask, self.o_mask))

    def get_legal_moves(self) -> List[int]:
        return [i for i in range(9) if not self.x_mask[i] and not self.o_mask[i]]

    def make_move(self, pos: int, is_x: bool) -> "Board":
        x_list = list(self.x_mask)
        o_list = list(self.o_mask)
        if is_x: x_list[pos] = True
        else: o_list[pos] = True
        return Board(tuple(x_list), tuple(o_list))

class TicTacToeSolver:
    def __init__(self):
        self.history: Dict[Tuple, Result] = {}

    def solve(self, board: Board, is_turn_x: bool) -> Result:
        state_id = board.get_canonical_state()
        if state_id in self.history:
            return self.history[state_id]

        if board.is_win(True): return Result(x_win=1)
        if board.is_win(False): return Result(o_win=1)
        if board.is_full(): return Result(draw=1)

        total_result = Result()
        for pos in board.get_legal_moves():
            next_board = board.make_move(pos, is_turn_x)
            total_result += self.solve(next_board, not is_turn_x)

        self.history[state_id] = total_result
        return total_result

class TicTacToeCPU:
    def __init__(self):
        self.solver = TicTacToeSolver()

    def get_possible_moves(self, board: Board, is_x: bool) -> Dict[int, Tuple[float, float]]:
        move_distribution = {}
        legal_moves = board.get_legal_moves()
        if not legal_moves:
            return move_distribution

        for pos in legal_moves:
            next_state = board.make_move(pos, is_x)
            
            if next_state.is_win(is_x):
                move_distribution[pos] = (1.0, 0.0)
                continue
            
            res = self.solver.solve(next_state, not is_x)
            total = res.x_win + res.o_win + res.draw
            
            win_count = res.x_win if is_x else res.o_win
            win_score = win_count / total if total > 0 else 0
            draw_score = res.draw / total if total > 0 else 0
            move_distribution[pos] = (win_score, draw_score)
        return move_distribution


from abc import ABC, abstractmethod


class TicTacToeStrategy(ABC):
    def __init__(self, cpu: Optional[TicTacToeCPU] = None):
        self.cpu = cpu or TicTacToeCPU()

    def get_move(self, board: list[list[Player]], is_x: bool) -> Tuple[int, int]:
        b = Board.from_list(board)
        move = self.strategy(b, is_x)
        if move is None:
            return -1, -1
        return move // 3, move % 3

    @abstractmethod
    def strategy(self, board: Board, is_x: bool) -> int:
        pass

class StochasticStrategy(TicTacToeStrategy):
    def __init__(self, cpu: Optional[TicTacToeCPU] = None, temperature: float = 0.01):
        super().__init__(cpu)
        self.temperature = temperature

    def strategy(self, board: Board, is_x: bool) -> int:
        move_distribution = self.cpu.get_possible_moves(board, is_x)
        if not move_distribution:
            return None
        
        moves = []
        logits = []
        for move, (win_score, draw_score) in move_distribution.items():
            moves.append(move)
            logits.append((win_score - draw_score) / self.temperature)
            if win_score == 1:
                return move
        
        max_logit = max(logits)
        exp_logits = [math.exp(l - max_logit) for l in logits]
        sum_exp = sum(exp_logits)
        probs = [e / sum_exp for e in exp_logits]
        
        chosen_move = random.choices(moves, weights=probs, k=1)[0]
        return chosen_move

class GreedyStrategy(TicTacToeStrategy):
    def strategy(self, board: Board, is_x: bool) -> int:
        move_distribution = self.cpu.get_possible_moves(board, is_x)
        
        best_move = None
        best_score = (-1, -1)
        for move, score in move_distribution.items():
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

class RandomStrategy(TicTacToeStrategy):
    def strategy(self, board: Board, is_x: bool) -> int:
        move_distribution = self.cpu.get_possible_moves(board, is_x)
        if not move_distribution:
            return None
        
        moves = list(move_distribution.keys())
        chosen_move = random.choice(moves)
        return chosen_move

class RandomSmartStrategy(TicTacToeStrategy):
    def strategy(self, board: Board, is_x: bool) -> int:
        move_distribution = self.cpu.get_possible_moves(board, is_x)
        if not move_distribution:
            return None
        
        moves = list(move_distribution.keys())
        for move in moves:
            if move_distribution[move][0] == 1:
                return move
        return random.choice(moves)

# Strategies
class DummyStrategy(RandomStrategy):
    pass

class BeginnerStrategy(RandomSmartStrategy):
    pass

class IntermediateStrategy(StochasticStrategy):
    def __init__(self, cpu: Optional[TicTacToeCPU] = None, temperature: float = 1.0):
        super().__init__(cpu, temperature)

class AdvancedStrategy(StochasticStrategy):
    def __init__(self, cpu: Optional[TicTacToeCPU] = None, temperature: float = 0.1):
        super().__init__(cpu, temperature)

class HardcoreStrategy(GreedyStrategy):
    pass
