import pytest
from app.logic.elo import EloEngine

def test_elo_win():
    # Player 1 wins (score 1.0)
    # Both start at 1200
    r1, r2 = EloEngine.compute(1200, 1200, 1.0)
    assert r1 > 1200
    assert r2 < 1200
    assert r1 + r2 == 2400

def test_elo_draw():
    # Draw (score 0.5)
    r1, r2 = EloEngine.compute(1200, 1200, 0.5)
    assert r1 == 1200
    assert r2 == 1200

def test_elo_unbalanced():
    # High rated player wins against low rated player
    r1, r2 = EloEngine.compute(2000, 1200, 1.0)
    diff = r1 - 2000
    
    # Low rated player wins against high rated player
    r3, r4 = EloEngine.compute(2000, 1200, 0.0)
    diff2 = r4 - 1200 # increase in rating for the winner
    
    assert diff2 > diff # Winner gets more points when defeating stronger opponent
