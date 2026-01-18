import dataclasses
from datetime import datetime

from sqlalchemy import JSON, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import composite, relationship

from backend.db.database import Base


@dataclasses.dataclass
class PlayerState:
    id: int
    name: str
    secret: str
    guesses: list
    elo: int

    # Required by SQLAlchemy to map attributes back to columns
    def __composite_values__(self):
        return self.id, self.name, self.secret, self.guesses, self.elo


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True)
    game_type = Column(String)  # 'pvp' or 'single'

    __mapper_args__ = {"polymorphic_identity": "games", "polymorphic_on": game_type}


class SingleGame(Game):
    __tablename__ = "single_games"
    id = Column(Integer, ForeignKey("games.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "single"}

    # --- Player 1 Columns & Composite ---
    _p_id = Column("player1_id", Integer, ForeignKey("users.id"), nullable=False)
    _p_name = Column("player1_name", String, nullable=True)
    _p_secret = Column("player1_secret", String(4), nullable=True)
    _p_guesses = Column("player1_guesses", JSON, default=list, nullable=False)
    _p_elo = Column("player1_elo", Integer, nullable=False)
    # This creates the nested structure: game.player.secret
    player = composite(PlayerState, _p_id, _p_name, _p_secret, _p_guesses, _p_elo)

    # --- Other Fields ---
    game_mode = Column(String, nullable=False)
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="waiting", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # --- Relationships ---
    player_user = relationship("User", foreign_keys=[_p_id])
    winner = relationship("User", foreign_keys=[winner_id])


class PvPGame(Game):
    __tablename__ = "pvp_games"
    id = Column(Integer, ForeignKey("games.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "pvp"}

    # --- Player 1 Columns & Composite ---
    _p1_id = Column("player1_id", Integer, ForeignKey("users.id"), nullable=False)
    _p1_name = Column("player1_name", String, nullable=True)
    _p1_secret = Column("player1_secret", String(4), nullable=True)
    _p1_guesses = Column("player1_guesses", JSON, default=list, nullable=False)
    _p1_elo = Column("player1_elo", Integer, nullable=False)
    # This creates the nested structure: game.player1.secret
    player1 = composite(PlayerState, _p1_id, _p1_name, _p1_secret, _p1_guesses, _p1_elo)

    # --- Player 2 Columns & Composite ---
    _p2_id = Column("player2_id", Integer, ForeignKey("users.id"), nullable=True)
    _p2_name = Column("player2_name", String, nullable=True)
    _p2_secret = Column("player2_secret", String(4), nullable=True)
    _p2_guesses = Column("player2_guesses", JSON, default=list, nullable=False)
    _p2_elo = Column("player2_elo", Integer, nullable=True)
    # This creates the nested structure: game.player2.secret
    player2 = composite(PlayerState, _p2_id, _p2_name, _p2_secret, _p2_guesses, _p2_elo)

    # --- Other Fields ---
    game_mode = Column(String, nullable=False)
    ai_difficulty = Column(String, nullable=True)
    current_turn = Column(Integer, default=1, nullable=False)
    starter_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    status = Column(String, default="waiting", nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # --- Relationships ---
    player1_user = relationship("User", foreign_keys=[_p1_id])
    player2_user = relationship("User", foreign_keys=[_p2_id])
    winner = relationship("User", foreign_keys=[winner_id])
