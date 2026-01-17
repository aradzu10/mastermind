from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict, Field


class GameCreate(BaseModel):
    game_mode: str = Field(default="single", pattern="^(single|ai|pvp)$")
    # For PVP or AI
    player_secret: Optional[str] = Field(None, min_length=4, max_length=4, pattern="^[0-9]{4}$")
    # For AI
    ai_difficulty: Optional[str] = Field(None, pattern="^(easy|medium|hard)$")


class GameGuess(BaseModel):
    guess: str = Field(..., min_length=4, max_length=4, pattern="^[0-9]{4}$")


class GuessRecord(BaseModel):
    guess: str = Field(..., min_length=4, max_length=4, pattern="^[0-9]{4}$")
    exact: int = Field(..., ge=0, le=4)
    wrong_pos: int = Field(..., ge=0, le=4)


class GameResponse(BaseModel):
    id: int
    game_mode: str

    self_id: int
    self_name: str
    self_secret: Optional[str]
    self_guesses: List[GuessRecord]

    winner_id: Optional[int]
    created_at: datetime
    completed_at: Optional[datetime]

    # PvP Specific
    opponent_id: Optional[int]
    opponent_name: Optional[str]
    opponent_secret: Optional[str]
    opponent_guesses: Optional[List[GuessRecord]]
    current_turn: Optional[int]
    status: Optional[str]
    started_at: Optional[datetime]

    # AI Specific
    ai_difficulty: Optional[str]
