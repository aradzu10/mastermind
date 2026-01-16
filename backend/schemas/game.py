from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional
from datetime import datetime


class GuessRecord(BaseModel):
    guess: str = Field(..., min_length=4, max_length=4, pattern="^[0-9]{4}$")
    exact: int = Field(..., ge=0, le=4)
    wrong_pos: int = Field(..., ge=0, le=4)


class GameCreate(BaseModel):
    game_mode: str = Field(default="single", pattern="^(single|ai_easy|ai_medium|ai_hard)$")


class GameGuess(BaseModel):
    guess: str = Field(..., min_length=4, max_length=4, pattern="^[0-9]{4}$")


class GameResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: Optional[int]
    attempts: int
    won: bool
    game_mode: str
    guesses: List[GuessRecord]
    completed_at: Optional[datetime]
    created_at: datetime


class GameGuessResponse(BaseModel):
    game_id: int
    guess: str
    exact: int
    wrong_pos: int
    is_winner: bool
    attempts: int
    game_over: bool
