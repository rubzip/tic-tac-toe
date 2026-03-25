from app.core.constants import Player, GameStatus, UsablePlayer


class TicTacToeEngine:
    @staticmethod
    def get_game_status(board: list[list[Player]]) -> GameStatus:
        # Check rows and columns
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] != Player.NONE:
                return (
                    GameStatus.WIN_X
                    if board[i][0] == Player.X
                    else GameStatus.WIN_O
                )
            if board[0][i] == board[1][i] == board[2][i] != Player.NONE:
                return (
                    GameStatus.WIN_X
                    if board[0][i] == Player.X
                    else GameStatus.WIN_O
                )

        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != Player.NONE:
            return (
                GameStatus.WIN_X if board[1][1] == Player.X else GameStatus.WIN_O
            )
        if board[0][2] == board[1][1] == board[2][0] != Player.NONE:
            return (
                GameStatus.WIN_X if board[1][1] == Player.X else GameStatus.WIN_O
            )

        # Check for draw or keep playing
        if any(Player.NONE in row for row in board):
            return GameStatus.KEEP_PLAYING

        return GameStatus.DRAW


class Game:
    def __init__(self, start_player: UsablePlayer = Player.O):
        self.board = [[Player.NONE for _ in range(3)] for _ in range(3)]
        self.turn: Player = start_player
    
    @classmethod
    def load(cls, board: list[list[Player]], turn: Player) -> 'Game':
        status = TicTacToeEngine.get_game_status(board)
        
        x_count = sum(row.count(Player.X) for row in board)
        o_count = sum(row.count(Player.O) for row in board)
        
        if abs(x_count - o_count) > 1:
            raise ValueError("Invalid board: turn count imbalance.")
        if x_count > o_count and turn == Player.X:
            raise ValueError("Invalid board: turn must be X.")
        if x_count < o_count and turn == Player.O:
            raise ValueError("Invalid board: turn must be O.")

        if status != GameStatus.KEEP_PLAYING:
            turn = Player.NONE
        elif turn == Player.NONE:
            raise ValueError("Game is ongoing; turn must be X or O.")
        
        game = cls()
        game.board = [row[:] for row in board]
        game.turn = turn
        return game

    def put(self, x: int, y: int, player: UsablePlayer):
        if self.get_game_status() != GameStatus.KEEP_PLAYING:
            raise ValueError("Game is already over")
        if not (0 <= x < 3 and 0 <= y < 3):
            raise ValueError(f"Invalid coordinates ({x}, {y})")
        if self.board[x][y] != Player.NONE:
            raise ValueError(f"Occupied cell ({x}, {y})")
        if player != self.turn:
            raise ValueError(f"Now is {self.turn} turn")

        self.board[x][y] = player
        self.turn = Player.O if player == Player.X else Player.X
        if self.get_game_status() != GameStatus.KEEP_PLAYING:
            self.turn = Player.NONE
    
    def get_turn(self) -> UsablePlayer:
        return self.turn
    
    def get_board(self) -> list[list[Player]]:
        return self.board
    
    def get_game_status(self) -> GameStatus:
        return TicTacToeEngine.get_game_status(self.board)
