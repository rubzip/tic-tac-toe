class EloEngine:
    @staticmethod
    def compute(r1: float, r2: float, score1: float, k: float = 32.0) -> tuple[float, float]:
        """
        Computes new Elo of 2 players.
        
        :param r1: actual Elo player 1
        :param r2: actual Elo player 2
        :param score1: Player 1 Score (1.0 = Win, 0.5 = Draw, 0.0 = Loss)
        :param k: Factor K (volatility). 32 is standard.
        """
        if not 0 <= score1 <= 1:
            raise ValueError

        q1 = EloEngine.compute_q(r1)
        q2 = EloEngine.compute_q(r2)
        
        e1 = q1 / (q1 + q2)
        e2 = q2 / (q1 + q2)

        score2 = 1.0 - score1

        new_r1 = r1 + k * (score1 - e1)
        new_r2 = r2 + k * (score2 - e2)

        return new_r1, new_r2

    @staticmethod
    def compute_q(x: float) -> float:
        return 10. ** (x / 400.)
