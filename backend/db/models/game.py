from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    secret = Column(String(4), nullable=False)  # The code player is guessing (AI/computer's secret)
    player_secret = Column(String(4), nullable=True)  # The player's code (for AI to guess)
    attempts = Column(Integer, default=0, nullable=False)
    won = Column(Boolean, default=False, nullable=False)
    game_mode = Column(String, default="single", nullable=False)  # single, ai, pvp
    guesses = Column(JSON, default=list, nullable=False)  # Player's guesses: [{guess, exact, wrong_pos}]
    ai_guesses = Column(JSON, default=list, nullable=True)  # AI's guesses: [{guess, exact, wrong_pos}]
    opponent_type = Column(String, default="none", nullable=False)  # none, ai, human
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="games")
