from .schemas import Player, UsablePlayer, GameStatus, GameState, Move


class TicTacToe:
    def __init__(self, start_player: UsablePlayer = Player.O):
        self.board = [[Player.NONE for _ in range(3)] for _ in range(3)]
        self.turn: UsablePlayer = start_player

    def put(self, move: Move, player: UsablePlayer):
        if self.board[move.row][move.col] != Player.NONE:
            raise ValueError("Occupied cell")
        if player != self.turn:
            raise ValueError(f"Now is {self.turn} turn")

        self.board[move.row][move.col] = player
        self.turn = Player.O if player == Player.X else Player.X

    def get_game_status(self) -> GameStatus:
        # Check rows and columns
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] != Player.NONE:
                return (
                    GameStatus.WIN_X
                    if self.board[i][0] == Player.X
                    else GameStatus.WIN_O
                )
            if self.board[0][i] == self.board[1][i] == self.board[2][i] != Player.NONE:
                return (
                    GameStatus.WIN_X
                    if self.board[0][i] == Player.X
                    else GameStatus.WIN_O
                )

        # Check diagonals
        if self.board[0][0] == self.board[1][1] == self.board[2][2] != Player.NONE:
            return (
                GameStatus.WIN_X if self.board[1][1] == Player.X else GameStatus.WIN_O
            )
        if self.board[0][2] == self.board[1][1] == self.board[2][0] != Player.NONE:
            return (
                GameStatus.WIN_X if self.board[1][1] == Player.X else GameStatus.WIN_O
            )

        # Check for draw or keep playing
        if any(Player.NONE in row for row in self.board):
            return GameStatus.KEEP_PLAYING

        return GameStatus.DRAW

    def get_state(self) -> GameState:
        return GameState(
            board=self.board, turn=self.turn, status=self.get_game_status()
        )
