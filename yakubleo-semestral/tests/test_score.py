"""Test score class"""

from app.score import Score


def test_score_initialization():
    """Tests initializing a Score object."""
    score = Score()
    assert score.score == 0


def test_score_increment():
    """Tests incrementing the score."""

    score = Score()

    score.increment()
    assert score.score == 1

    score.increment()
    assert score.score == 2
