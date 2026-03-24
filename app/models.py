from .schemas import Player, UsablePlayer, GameStatus, GameState, Move


class TicTacToe:
    def __init__(self, start_player: UsablePlayer = Player.O):
        self.board = [[Player.NONE for _ in range(3)] for _ in range(3)]
        self.turn: UsablePlayer = start_player

    def put(self, move: Move, player: UsablePlayer):
        if self.get_game_status() != GameStatus.KEEP_PLAYING:
            raise 
        if self.board[move.row][move.col] != Player.NONE:
            raise ValueError("Occupied cell")
        if player != self.turn:
            raise ValueError(f"Now is {self.turn} turn")

        self.board[move.row][move.col] = player
        self.turn = Player.O if player == Player.X else Player.X

    def get_state(self) -> GameState:
        return GameState(
            board=self.board, turn=self.turn, status=self.get_game_status()
        )
    
    def get_game_status(self) -> GameStatus:
        return TicTacToeEngine.get_game_status(self.board)

class TicTacToeEngine:
    @staticmethod
    def get_game_status(board) -> GameStatus:
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
