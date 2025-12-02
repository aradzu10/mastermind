"""Tests for the database module."""

import tempfile
from pathlib import Path

from database import ScoreRecord, ScoreRepository, GameRecordManager


def test_score_record_to_dict():
    record = ScoreRecord(
        player_name="Alice",
        guesses=5,
        secret="1234",
    )
    data = record.to_dict()
    assert data["player_name"] == "Alice"
    assert data["guesses"] == 5
    assert data["secret"] == "1234"


def test_score_record_from_dict():
    data = {
        "player_name": "Bob",
        "guesses": 3,
        "secret": "5678",
    }
    record = ScoreRecord.from_dict(data)
    assert record.player_name == "Bob"
    assert record.guesses == 3
    assert record.secret == "5678"


def test_repository_save_and_load():
    with tempfile.NamedTemporaryFile(suffix=".json") as f:
        temp_path = Path(f.name)

        repo = ScoreRepository(temp_path)
        record = ScoreRecord(player_name="Alice", guesses=5, secret="1234")
        repo.save_score(record)

        scores = repo.get_scores()
        assert len(scores) == 1
        assert scores[0].player_name == "Alice"
        assert scores[0].guesses == 5


def test_manager_get_high_score():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        temp_path = Path(f.name)

        manager = GameRecordManager(temp_path)
        manager.record_score("Alice", 10, "1111")
        manager.record_score("Bob", 3, "2222")
        manager.record_score("Charlie", 7, "3333")

        high_score = manager.get_high_score()
        assert high_score is not None
        assert high_score.player_name == "Bob"
        assert high_score.guesses == 3


def test_manager_returns_true_for_new_high_score():
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        temp_path = Path(f.name)

        manager = GameRecordManager(temp_path)
        assert manager.record_score("Alice", 10, "1234") is True  # First score
        assert manager.record_score("Bob", 5, "5678") is True  # New high score
        assert manager.record_score("Charlie", 8, "9999") is False  # Not a high score
