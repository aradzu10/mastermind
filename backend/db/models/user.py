from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String
from sqlalchemy.orm import relationship

from backend.db.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=True)
    google_id = Column(String, unique=True, index=True, nullable=True)
    display_name = Column(String, nullable=False)
    is_guest = Column(Boolean, default=False, nullable=False)
    elo_rating = Column(Float, default=1200.0, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    single_games = relationship(
        "SingleGame",
        foreign_keys="SingleGame._p_id",
        back_populates="player_user",
        viewonly=True,
    )
    pvp_games = relationship(
        "PvPGame",
        primaryjoin="or_(User.id==PvPGame._p1_id, User.id==PvPGame._p2_id)",
        foreign_keys="[PvPGame._p1_id, PvPGame._p2_id]",
        viewonly=True,
    )
