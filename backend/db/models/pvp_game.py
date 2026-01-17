from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from backend.db.database import Base


class PvPGame(Base):
    __tablename__ = "pvp_games"

    id = Column(Integer, primary_key=True, index=True)
    player1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null until player 2 joins
    player1_secret = Column(String(4), nullable=True)  # Set during setup phase
    player2_secret = Column(String(4), nullable=True)  # Set during setup phase
    player1_guesses = Column(JSON, default=list, nullable=False)  # List of {guess, exact, wrong_pos}
    player2_guesses = Column(JSON, default=list, nullable=False)  # List of {guess, exact, wrong_pos}
    current_turn = Column(Integer, default=1, nullable=False)  # 1 or 2
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="waiting", nullable=False)  # waiting, setting_secrets, in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)  # When both secrets are set
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    player1 = relationship("User", foreign_keys=[player1_id])
    player2 = relationship("User", foreign_keys=[player2_id])
    winner = relationship("User", foreign_keys=[winner_id])
