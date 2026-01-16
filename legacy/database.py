"""
Database module for Mastermind game.

This module provides an extensible database architecture for storing game data.
It uses the Repository pattern with abstract base classes to allow easy
swapping of storage implementations (JSON, SQLite, cloud, etc.).
"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import json
from typing import Optional


@dataclass
class ScoreRecord:
    """Represents a single score record."""

    player_name: str
    guesses: int
    secret: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "player_name": self.player_name,
            "guesses": self.guesses,
            "secret": self.secret,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "ScoreRecord":
        """Create ScoreRecord from dictionary."""
        return cls(
            player_name=data["player_name"],
            guesses=data["guesses"],
            secret=data["secret"],
            timestamp=data.get("timestamp", datetime.now().isoformat()),
        )


class ScoreRepository:
    def __init__(self, file_path: Optional[str | Path] = None):
        self.file_path = Path(file_path if file_path else "scores.json.db")

    def _load_data(self) -> dict:
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"scores": []}

    def _save_data(self, data: dict) -> None:
        with open(self.file_path, "w") as f:
            json.dump(data, f, indent=2)

    def get_scores(self) -> list[ScoreRecord]:
        data = self._load_data()
        return [ScoreRecord.from_dict(record) for record in data.get("scores", [])]

    def save_score(self, record: ScoreRecord) -> list[ScoreRecord]:
        data = self._load_data()
        data["scores"].append(record.to_dict())
        self._save_data(data)
        return [ScoreRecord.from_dict(record) for record in data.get("scores", [])]


class GameRecordManager:
    """
    High-level manager for game scores.

    Uses dependency injection to accept any ScoreRepository implementation.
    This allows easy switching between storage backends.
    """

    def __init__(self, file_path: Optional[str | Path] = None):
        self.repository = ScoreRepository(file_path)
        self.scores = self.repository.get_scores()

    def record_score(self, player_name: str, guesses: int, secret: str) -> bool:
        current_high = self.get_high_score()
        is_new_high_score = current_high is None or guesses < current_high.guesses

        record = ScoreRecord(player_name=player_name, guesses=guesses, secret=secret)
        self.scores = self.repository.save_score(record)

        return is_new_high_score

    def get_high_score(self) -> Optional[ScoreRecord]:
        if not self.scores:
            return None
        return min(self.scores, key=lambda x: x.guesses)