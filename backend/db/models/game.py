from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from datetime import datetime
from backend.db.database import Base


class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    secret = Column(String(4), nullable=False)
    attempts = Column(Integer, default=0, nullable=False)
    won = Column(Boolean, default=False, nullable=False)
    game_mode = Column(String, default="single", nullable=False)  # single, ai_easy, ai_medium, ai_hard
    guesses = Column(JSON, default=list, nullable=False)  # List of {guess, exact, wrong_pos}
    completed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    user = relationship("User", back_populates="games")
